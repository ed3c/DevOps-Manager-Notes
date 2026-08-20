#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import compile_public_receipt_packet as core

SAFE_SECRET_SENTINELS = core.SAFE_SECRET_SENTINELS
EXTRA_SENSITIVE_KEYS = {
    "authorization",
    "bearer",
    "access_token",
    "refresh_token",
    "id_token",
    "session_token",
    "session_cookie",
    "cookie",
    "set_cookie",
}
MAX_RECEIPT_ROOTS = 8
LIVE_OUTPUT_ROOT = Path("evidence/local-handoff")


def sensitive_value_is_safe(value: Any) -> bool:
    if value in (None, False):
        return True
    return isinstance(value, str) and value.upper() in SAFE_SECRET_SENTINELS


def assert_extended_sensitive_keys(value: Any, *, label: str) -> None:
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for raw_key, child in node.items():
                key = str(raw_key).lower().replace("-", "_")
                if key in EXTRA_SENSITIVE_KEYS and not sensitive_value_is_safe(child):
                    raise ValueError(
                        f"{label} contains non-redacted sensitive key at {path}.{raw_key}"
                    )
                walk(child, f"{path}.{raw_key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")

    walk(value, "$")


def validate_queue_progress(items: list[dict[str, Any]], queue: dict[str, Any]) -> int:
    active_id = queue["current"]["active_item"]
    active_index = next(
        index for index, item in enumerate(items) if item["id"] == active_id
    )
    for index, item in enumerate(items):
        state = item.get("state")
        if index < active_index and state != "COMPLETE":
            raise ValueError(
                f"queue item {item['id']} precedes ACTIVE item but is not COMPLETE"
            )
        if index == active_index and state != "ACTIVE":
            raise ValueError(f"queue item {item['id']} must be ACTIVE")
        if index > active_index and state != "BLOCKED_BY_PREDECESSOR":
            raise ValueError(
                f"queue item {item['id']} follows ACTIVE item but is not BLOCKED_BY_PREDECESSOR"
            )
    return active_index


def validate_receipt_roots(roots: list[Path]) -> list[Path]:
    if not roots:
        raise ValueError("at least one explicit --receipt-root is required")
    if len(roots) > MAX_RECEIPT_ROOTS:
        raise ValueError(f"at most {MAX_RECEIPT_ROOTS} receipt roots are allowed")
    resolved: list[Path] = []
    for root in roots:
        value = root.resolve()
        if not value.is_dir():
            raise ValueError(f"receipt root is not a directory: {value}")
        if value == Path(value.anchor):
            raise ValueError("filesystem root cannot be admitted as a receipt root")
        resolved.append(value)
    if len({str(root) for root in resolved}) != len(resolved):
        raise ValueError("receipt roots must be unique")
    return resolved


def resolve_output_path(repo_root: Path, value: str, *, fixture_mode: bool) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    resolved = path.resolve()
    if not fixture_mode:
        allowed = (repo_root / LIVE_OUTPUT_ROOT).resolve()
        if not core.is_within(resolved, allowed):
            raise ValueError(
                "live public packet output must remain under evidence/local-handoff"
            )
    return resolved


def protected_input_paths(
    *,
    queue_path: Path,
    roots: list[Path],
    assignments: dict[str, str],
) -> set[Path]:
    result = {queue_path.resolve()}
    for value in assignments.values():
        path, _, _ = core.resolve_receipt_path(value, roots=roots)
        result.add(path.resolve())
    return result


def admit_packet(
    *,
    repo_root: Path,
    queue_path: Path,
    receipt_roots: list[Path],
    receipt_assignments: dict[str, str],
    max_receipt_bytes: int,
    fixture_mode: bool,
) -> dict[str, Any]:
    queue, _ = core.load_json_file(
        queue_path.resolve(), max_bytes=core.HARD_MAX_RECEIPT_BYTES
    )
    items = core.validate_queue(queue)
    active_index = validate_queue_progress(items, queue)

    prefix_ids = [str(item["id"]) for item in items[: len(receipt_assignments)]]
    if set(receipt_assignments) != set(prefix_ids):
        raise ValueError("receipt assignments must form a contiguous prefix")
    if len(receipt_assignments) > active_index + 1:
        blocked = items[active_index + 1]["id"]
        raise ValueError(
            f"receipt for blocked future item is forbidden before queue advancement: {blocked}"
        )

    packet = core.compile_packet(
        repo_root=repo_root,
        queue_path=queue_path,
        receipt_roots=receipt_roots,
        receipt_assignments=receipt_assignments,
        max_receipt_bytes=max_receipt_bytes,
        fixture_mode=fixture_mode,
    )

    for index, entry in enumerate(packet["receipts"]):
        if index < active_index and entry["verdict"] != "PASS":
            raise ValueError(
                f"completed queue item {entry['item_id']} cannot carry a FAIL receipt"
            )
        source_path, _, _ = core.resolve_receipt_path(
            receipt_assignments[entry["item_id"]], roots=receipt_roots
        )
        receipt, raw = core.load_json_file(
            source_path, max_bytes=max_receipt_bytes
        )
        core.assert_public_safe(
            receipt, raw.decode("utf-8"), label=f"receipt {entry['item_id']}"
        )
        assert_extended_sensitive_keys(
            receipt, label=f"receipt {entry['item_id']}"
        )

    if len(packet["receipts"]) == active_index:
        packet["aggregate"]["state"] = "ACTIVE_RECEIPT_REQUIRED"
        packet["aggregate"]["next_item"] = items[active_index]["id"]

    packet["admission_policy"] = {
        "queue_state_shape": "COMPLETE* -> ACTIVE -> BLOCKED_BY_PREDECESSOR*",
        "future_blocked_receipts_accepted": False,
        "completed_fail_receipts_accepted": False,
        "live_output_root": str(LIVE_OUTPUT_ROOT),
        "queue_or_receipt_overwrite_allowed": False,
        "max_receipt_roots": MAX_RECEIPT_ROOTS,
    }
    core.assert_public_safe(
        packet,
        core.canonical_bytes(packet).decode("utf-8"),
        label="public packet",
    )
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Authoritative M9 admission CLI: validate one current Local Handoff "
            "queue frontier and emit a bounded public-safe receipt projection."
        )
    )
    parser.add_argument("--queue", default="handoff/local-handoff-queue.json")
    parser.add_argument("--receipt-root", action="append", default=[])
    parser.add_argument("--receipt", action="append", default=[], metavar="ITEM_ID=PATH")
    parser.add_argument(
        "--output",
        default="evidence/local-handoff/public-receipt-packet.json",
    )
    parser.add_argument(
        "--max-receipt-bytes",
        type=int,
        default=core.DEFAULT_MAX_RECEIPT_BYTES,
    )
    parser.add_argument("--fixture-mode", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    try:
        queue_path = core.resolve_live_path(
            repo_root, args.queue, fixture_mode=False
        )
        assignments = core.parse_receipt_assignments(args.receipt)
        raw_roots = [
            Path(value) if Path(value).is_absolute() else repo_root / value
            for value in args.receipt_root
        ]
        roots = validate_receipt_roots(raw_roots)
        output = resolve_output_path(
            repo_root, args.output, fixture_mode=args.fixture_mode
        )
        if output in protected_input_paths(
            queue_path=queue_path,
            roots=roots,
            assignments=assignments,
        ):
            raise ValueError("public packet output must not overwrite queue or receipt input")

        packet = admit_packet(
            repo_root=repo_root,
            queue_path=queue_path,
            receipt_roots=roots,
            receipt_assignments=assignments,
            max_receipt_bytes=args.max_receipt_bytes,
            fixture_mode=args.fixture_mode,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(core.canonical_bytes(packet))
        print(
            json.dumps(
                {
                    "output": str(output),
                    "state": packet["aggregate"]["state"],
                    "evidence_kind": packet["evidence_kind"],
                    "evidence_ceiling": packet["evidence_ceiling"],
                    "queue_advanced": False,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"receipt-admission-error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
