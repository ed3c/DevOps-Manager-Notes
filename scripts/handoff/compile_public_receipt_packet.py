#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPOSITORY = "ed3c/DevOps-Manager-Notes"
QUEUE_SCHEMA = "agentic-tech-lead/local-handoff-queue/v1"
PACKET_SCHEMA = "full-manager-mvp/public-local-receipt-packet/v1"
LIVE_PACKET_CEILING = "PUBLIC_SAFE_LOCAL_RECEIPT_PROJECTION_ONLY"
FIXTURE_PACKET_CEILING = "FIXTURE_PUBLIC_RECEIPT_PACKET_ONLY"
DEFAULT_MAX_RECEIPT_BYTES = 1_000_000
HARD_MAX_RECEIPT_BYTES = 2_000_000
SHA40_RE = re.compile(r"[0-9a-f]{40}")
CHECK_KEY_RE = re.compile(r"[A-Za-z0-9_.-]{1,100}")
SECRET_KEY_RE = re.compile(
    r"(?:pass(?:word|wd)|token|api[_-]?key|private[_-]?key|secret|"
    r"client[_-]?secret|access[_-]?key|credential(?:s)?)",
    re.IGNORECASE,
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
)
SAFE_SECRET_SENTINELS = {
    "",
    "NO",
    "NONE",
    "ABSENT",
    "NOT_EXERCISED",
    "REDACTED",
    "EXTERNALIZED",
    "REQUIRED_AT_RUNTIME",
    "SKIPPED_BY_POLICY",
}


@dataclass(frozen=True)
class ReceiptSpec:
    verdict_field: str
    live_ceiling: str
    fixture_ceiling: str | None
    pass_checks: dict[str, frozenset[str]]
    cleanup_checks: dict[str, frozenset[str]]
    summary_kind: str


def exact_values(*values: str) -> frozenset[str]:
    return frozenset(values)


SPECS: dict[str, ReceiptSpec] = {
    "full-manager-mvp/local-reviewer-handoff-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "reviewer_demo_pass_bounded": exact_values("PASS"),
            "seven_failure_drills": exact_values("PASS"),
            "same_failure_retest": exact_values("PASS"),
            "business_pass_fail_metrics_visible": exact_values("PASS"),
            "paid_api_required": exact_values("NO"),
        },
        cleanup_checks={"generated_workspace_cleanup": exact_values("PASS")},
        summary_kind="reviewer",
    ),
    "full-manager-mvp/local-kind-substrate-receipt/v1": ReceiptSpec(
        verdict_field="verdict",
        live_ceiling="LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "local_kind_cluster_created": exact_values("PASS"),
            "oci_digest_bound": exact_values("PASS"),
            "deployment_ready": exact_values("PASS"),
            "business_oracle_pass": exact_values("PASS"),
            "business_oracle_forced_fail_visible": exact_values("PASS"),
            "pod_image_ids_captured": exact_values("PASS"),
        },
        cleanup_checks={
            "cleanup": exact_values("PASS"),
            "kubectl_context_restored": exact_values(
                "PASS", "SKIPPED_NO_PRIOR_CONTEXT"
            ),
        },
        summary_kind="kind",
    ),
    "full-manager-mvp/m7-advanced-queue-compile-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_HANDOFF_QUEUE_COMPILATION_ONLY",
        fixture_ceiling="FIXTURE_COMPILER_CONTRACT_ONLY",
        pass_checks={},
        cleanup_checks={},
        summary_kind="queue_compile",
    ),
    "full-manager-mvp/local-argo-ephemeral-kind-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_ARGO_CONTROLLERS_READY_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "cluster_created": exact_values("PASS"),
            "inner_controller_receipt_pass": exact_values("PASS"),
            "inner_cleanup_pass": exact_values("PASS"),
        },
        cleanup_checks={
            "cluster_cleanup": exact_values("PASS"),
            "kubectl_context_restored": exact_values(
                "PASS", "SKIPPED_NO_PRIOR_CONTEXT"
            ),
        },
        summary_kind="argo",
    ),
    "full-manager-mvp/local-model-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "llama_commit_checked_out": exact_values("PASS"),
            "model_download_within_budget": exact_values("PASS"),
            "model_sha256_verified": exact_values("PASS"),
            "llama_cli_built": exact_values("PASS"),
            "local_inference_exit_zero": exact_values("PASS"),
            "local_inference_output_nonempty": exact_values("PASS"),
        },
        cleanup_checks={"cleanup": exact_values("PASS")},
        summary_kind="model",
    ),
    "full-manager-mvp/local-capacity-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_SYNTHETIC_1000_VU_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "loopback_port_free": exact_values("PASS"),
            "loopback_service_live": exact_values("PASS"),
            "locust_exit_zero": exact_values("PASS"),
            "aggregate_stats_present": exact_values("PASS"),
            "failure_ratio_within_limit": exact_values("PASS"),
            "p95_within_limit": exact_values("PASS"),
        },
        cleanup_checks={"cleanup": exact_values("PASS")},
        summary_kind="capacity",
    ),
    "full-manager-mvp/local-registry-signing-receipt/v1": ReceiptSpec(
        verdict_field="state",
        live_ceiling="LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY",
        fixture_ceiling=None,
        pass_checks={
            "cosign_binary_sha256_verified": exact_values("PASS"),
            "registry_started_from_exact_digest": exact_values("PASS"),
            "image_pushed_by_digest": exact_values("PASS"),
            "ephemeral_keypair_generated": exact_values("PASS"),
            "registry_signature_uploaded": exact_values("PASS"),
            "registry_signature_verified": exact_values("PASS"),
            "local_image_removed": exact_values("PASS"),
        },
        cleanup_checks={"cleanup": exact_values("PASS")},
        summary_kind="signing",
    ),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def exact_sha40(label: str, value: Any) -> str:
    if not isinstance(value, str) or not SHA40_RE.fullmatch(value):
        raise ValueError(f"{label} must be an exact lowercase 40-hex SHA")
    return value


def is_within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def load_json_file(path: Path, *, max_bytes: int) -> tuple[dict[str, Any], bytes]:
    if not path.is_file():
        raise ValueError(f"required JSON file is absent: {path}")
    size = path.stat().st_size
    if size <= 0:
        raise ValueError(f"JSON file is empty: {path}")
    if size > max_bytes:
        raise ValueError(
            f"receipt exceeds byte budget: {path} has {size}, max {max_bytes}"
        )
    raw = path.read_bytes()
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"receipt is not UTF-8: {path}") from exc
    try:
        value = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError(f"receipt is not valid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"receipt must contain one JSON object: {path}")
    return value, raw


def assert_public_safe(value: Any, raw_text: str, *, label: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(raw_text):
            raise ValueError(f"{label} contains secret-like material")

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                key_text = str(key)
                if SECRET_KEY_RE.fullmatch(key_text):
                    if isinstance(child, str) and child.upper() in SAFE_SECRET_SENTINELS:
                        pass
                    elif child in (None, False):
                        pass
                    else:
                        raise ValueError(
                            f"{label} contains non-redacted sensitive key at "
                            f"{path}.{key_text}"
                        )
                walk(child, f"{path}.{key_text}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")
        elif isinstance(node, str) and len(node) > 100_000:
            raise ValueError(f"{label} contains an unbounded string at {path}")

    walk(value, "$")


def git_subject(repo_root: Path) -> dict[str, str]:
    def git(*args: str) -> str:
        return subprocess.check_output(
            ["git", *args], cwd=repo_root, text=True, timeout=10
        ).strip()

    commit = exact_sha40("compiler commit", git("rev-parse", "HEAD"))
    tree = exact_sha40("compiler tree", git("rev-parse", "HEAD^{tree}"))
    return {"repository": REPOSITORY, "commit": commit, "tree": tree}


def validate_queue(queue: dict[str, Any]) -> list[dict[str, Any]]:
    if queue.get("schema_version") != QUEUE_SCHEMA:
        raise ValueError("queue schema mismatch")
    subject = queue.get("subject")
    if not isinstance(subject, dict):
        raise ValueError("queue subject must be an object")
    if subject.get("repository") != REPOSITORY:
        raise ValueError("queue repository subject mismatch")
    exact_sha40("queue commit", subject.get("commit"))
    exact_sha40("queue tree", subject.get("tree"))
    exact_sha40("queue rollback_commit", subject.get("rollback_commit"))

    items = queue.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("queue must contain at least one item")
    ids: list[str] = []
    active: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"queue item {index} must be an object")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            raise ValueError(f"queue item {index} has no stable id")
        if item_id in ids:
            raise ValueError(f"duplicate queue item id: {item_id}")
        ids.append(item_id)
        if item.get("state") == "ACTIVE":
            active.append(item_id)

        entry = item.get("entry", {})
        if entry.get("required_subject_commit") != subject["commit"]:
            raise ValueError(f"{item_id} required subject commit drifted")

        schema = item.get("receipt", {}).get("schema")
        if schema not in SPECS:
            raise ValueError(f"{item_id} receipt schema is unsupported: {schema!r}")

        expected_predecessor = None if index == 0 else items[index - 1].get("id")
        if entry.get("predecessor") != expected_predecessor:
            raise ValueError(f"{item_id} predecessor is not a linear queue edge")
        expected_next = None if index == len(items) - 1 else items[index + 1].get("id")
        if item.get("next") != expected_next:
            raise ValueError(f"{item_id} next edge is not linear")

    if len(active) != 1:
        raise ValueError(f"queue must contain exactly one ACTIVE item, got {active}")
    current = queue.get("current", {})
    if current.get("active_item") != active[0] or current.get("state") != "ACTIVE":
        raise ValueError("queue current pointer does not match the ACTIVE item")
    return items


def parse_receipt_assignments(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError("--receipt must use ITEM_ID=PATH")
        item_id, path = raw.split("=", 1)
        item_id = item_id.strip()
        path = path.strip()
        if not item_id or not path:
            raise ValueError("--receipt must use non-empty ITEM_ID=PATH")
        if item_id in result:
            raise ValueError(f"duplicate --receipt assignment for {item_id}")
        result[item_id] = path
    if not result:
        raise ValueError("at least one --receipt ITEM_ID=PATH is required")
    return result


def resolve_receipt_path(value: str, *, roots: list[Path]) -> tuple[Path, int, str]:
    candidate = Path(value)
    matches: list[tuple[Path, int, str]] = []
    if candidate.is_absolute():
        resolved = candidate.resolve()
        for index, root in enumerate(roots):
            if is_within(resolved, root) and resolved.is_file():
                matches.append((resolved, index, str(resolved.relative_to(root))))
    else:
        for index, root in enumerate(roots):
            resolved = (root / candidate).resolve()
            if is_within(resolved, root) and resolved.is_file():
                matches.append((resolved, index, str(resolved.relative_to(root))))
    if not matches:
        raise ValueError(
            f"receipt path is absent or outside every admitted receipt root: {value}"
        )
    unique = {(str(path), index, relative) for path, index, relative in matches}
    if len(unique) != 1:
        raise ValueError(f"receipt path is ambiguous across admitted roots: {value}")
    path_text, index, relative = next(iter(unique))
    return Path(path_text), index, relative


def expected_ceiling(spec: ReceiptSpec, *, fixture_mode: bool) -> str:
    if fixture_mode and spec.fixture_ceiling:
        return spec.fixture_ceiling
    return spec.live_ceiling


def require_check_values(
    checks: dict[str, Any],
    requirements: dict[str, frozenset[str]],
    *,
    label: str,
) -> dict[str, str]:
    selected: dict[str, str] = {}
    for key, allowed in requirements.items():
        value = checks.get(key)
        if value not in allowed:
            raise ValueError(
                f"{label} check {key} expected one of {sorted(allowed)}, got {value!r}"
            )
        selected[key] = str(value)
    return selected


def summary_mapping(source: Any, *, keys: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(source, dict):
        return {}
    result: dict[str, Any] = {}
    for key in keys:
        value = source.get(key)
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            if isinstance(value, str) and len(value) > 4000:
                raise ValueError(f"allowlisted summary value {key} is too large")
            result[key] = value
        elif isinstance(value, list):
            if len(value) > 100 or not all(
                isinstance(item, (str, int, float, bool)) for item in value
            ):
                raise ValueError(f"allowlisted summary list {key} is not bounded")
            result[key] = value
        else:
            raise ValueError(f"allowlisted summary value {key} is not scalar/list")
    return result


def extract_summary(receipt: dict[str, Any], kind: str) -> dict[str, Any]:
    if kind == "reviewer":
        return {"source_receipt": summary_mapping(receipt.get("source_receipt"), keys=("sha256", "schema_version", "verdict"))}
    if kind == "kind":
        return {"oci": summary_mapping(receipt.get("oci"), keys=("descriptor_digest", "immutable_image_ref", "media_type"))}
    if kind == "queue_compile":
        return {
            "predecessor_receipts": summary_mapping(receipt.get("predecessor_receipts"), keys=("reviewer_sha256", "kind_sha256")),
            "queue": summary_mapping(receipt.get("queue"), keys=("sha256", "active_item")),
            "physical_runtime_executed": receipt.get("physical_runtime_executed"),
        }
    if kind == "argo":
        return {"inner_receipt": summary_mapping(receipt.get("inner_receipt"), keys=("schema_version", "evidence_ceiling"))}
    if kind == "model":
        return {"inference": summary_mapping(receipt.get("inference"), keys=("output_sha256", "model_sha256", "model_bytes", "llama_commit", "model_license_id"))}
    if kind == "capacity":
        return {"result": summary_mapping(receipt.get("result"), keys=("users", "spawn_rate", "duration_seconds", "request_count", "failure_count", "failure_ratio", "p95_ms"))}
    if kind == "signing":
        return {"result": summary_mapping(receipt.get("result"), keys=("image_digest_ref", "registry_image", "cosign_binary_sha256", "ephemeral_public_key_sha256"))}
    raise ValueError(f"unsupported summary kind: {kind}")


def validate_receipt(
    *,
    item: dict[str, Any],
    receipt: dict[str, Any],
    queue_subject: dict[str, str],
    fixture_mode: bool,
) -> tuple[str, str, dict[str, str], dict[str, Any]]:
    item_id = str(item["id"])
    schema = receipt.get("schema_version")
    expected_schema = item.get("receipt", {}).get("schema")
    if schema != expected_schema:
        raise ValueError(
            f"{item_id} receipt schema mismatch: expected {expected_schema}, got {schema}"
        )
    spec = SPECS[schema]

    evidence_kind = receipt.get("evidence_kind")
    if fixture_mode:
        if evidence_kind != "FIXTURE":
            raise ValueError(f"{item_id} fixture receipt must declare evidence_kind=FIXTURE")
    elif evidence_kind == "FIXTURE":
        raise ValueError(f"{item_id} fixture receipt is forbidden in live admission mode")

    subject = receipt.get("subject")
    if not isinstance(subject, dict):
        raise ValueError(f"{item_id} receipt subject must be an object")
    for key in ("repository", "commit", "tree"):
        if subject.get(key) != queue_subject.get(key):
            raise ValueError(f"{item_id} receipt {key} does not match queue subject")

    verdict = receipt.get(spec.verdict_field)
    if verdict not in {"PASS", "FAIL"}:
        raise ValueError(f"{item_id} receipt {spec.verdict_field} must be PASS or FAIL")

    ceiling = receipt.get("evidence_ceiling")
    required_ceiling = expected_ceiling(spec, fixture_mode=fixture_mode)
    if ceiling != required_ceiling:
        raise ValueError(
            f"{item_id} evidence ceiling mismatch: expected {required_ceiling}, got {ceiling!r}"
        )

    checks = receipt.get("checks")
    if not isinstance(checks, dict):
        checks = {}
    selected: dict[str, str] = {}
    selected.update(require_check_values(checks, spec.cleanup_checks, label=item_id))
    if verdict == "PASS":
        selected.update(require_check_values(checks, spec.pass_checks, label=item_id))

    if schema == "full-manager-mvp/m7-advanced-queue-compile-receipt/v1":
        if receipt.get("physical_runtime_executed") is not False:
            raise ValueError(
                f"{item_id} compile receipt must record physical_runtime_executed=false"
            )
        expected_kind = "FIXTURE" if fixture_mode else "LIVE_PREDECESSOR_INPUTS"
        if receipt.get("evidence_kind") != expected_kind:
            raise ValueError(f"{item_id} compile receipt evidence_kind must be {expected_kind}")

    for key, value in selected.items():
        if not CHECK_KEY_RE.fullmatch(key) or not isinstance(value, str):
            raise ValueError(f"{item_id} selected check is not public-safe")

    return str(verdict), str(ceiling), dict(sorted(selected.items())), extract_summary(receipt, spec.summary_kind)


def compile_packet(
    *,
    repo_root: Path,
    queue_path: Path,
    receipt_roots: list[Path],
    receipt_assignments: dict[str, str],
    max_receipt_bytes: int,
    fixture_mode: bool,
) -> dict[str, Any]:
    if max_receipt_bytes < 1 or max_receipt_bytes > HARD_MAX_RECEIPT_BYTES:
        raise ValueError(f"--max-receipt-bytes must be between 1 and {HARD_MAX_RECEIPT_BYTES}")
    queue_resolved = queue_path.resolve()
    if not is_within(queue_resolved, repo_root.resolve()):
        raise ValueError("queue path must remain inside the repository")
    queue, queue_raw = load_json_file(queue_resolved, max_bytes=HARD_MAX_RECEIPT_BYTES)
    items = validate_queue(queue)
    item_by_id = {str(item["id"]): item for item in items}
    unknown = sorted(set(receipt_assignments) - set(item_by_id))
    if unknown:
        raise ValueError(f"receipt assignments reference unknown queue items: {unknown}")

    expected_prefix = [str(item["id"]) for item in items[: len(receipt_assignments)]]
    if set(receipt_assignments) != set(expected_prefix):
        raise ValueError("receipt assignments must form a contiguous prefix from the first queue item")

    roots = [root.resolve() for root in receipt_roots] or [repo_root.resolve()]
    if len(set(map(str, roots))) != len(roots):
        raise ValueError("receipt roots must be unique")

    queue_subject = queue["subject"]
    receipt_entries: list[dict[str, Any]] = []
    for item_id in expected_prefix:
        item = item_by_id[item_id]
        path, root_index, relative = resolve_receipt_path(receipt_assignments[item_id], roots=roots)
        receipt, raw = load_json_file(path, max_bytes=max_receipt_bytes)
        assert_public_safe(receipt, raw.decode("utf-8"), label=f"receipt {item_id}")
        verdict, ceiling, checks, summary = validate_receipt(
            item=item,
            receipt=receipt,
            queue_subject=queue_subject,
            fixture_mode=fixture_mode,
        )
        receipt_entries.append(
            {
                "item_id": item_id,
                "task_ref": item.get("task_ref"),
                "source": {
                    "root_alias": f"receipt_root_{root_index}",
                    "relative_path": relative,
                    "sha256": sha256_bytes(raw),
                    "bytes": len(raw),
                },
                "schema_version": receipt["schema_version"],
                "verdict": verdict,
                "evidence_ceiling": ceiling,
                "subject": {
                    "repository": receipt["subject"]["repository"],
                    "commit": receipt["subject"]["commit"],
                    "tree": receipt["subject"]["tree"],
                },
                "admitted_checks": checks,
                "public_summary": summary,
                "next_item": item.get("next"),
            }
        )

    failed = next((entry for entry in receipt_entries if entry["verdict"] == "FAIL"), None)
    if failed:
        aggregate_state = "LOCAL_GAP_OPEN"
        next_item = failed["item_id"]
    elif len(receipt_entries) == len(items):
        aggregate_state = "QUEUE_COMPLETION_REVIEW_REQUIRED"
        next_item = None
    else:
        aggregate_state = "HUMAN_QUEUE_ADVANCE_REQUIRED"
        next_item = str(items[len(receipt_entries)]["id"])

    packet = {
        "schema_version": PACKET_SCHEMA,
        "evidence_kind": "FIXTURE" if fixture_mode else "LIVE_LOCAL_RECEIPT_PROJECTION",
        "evidence_ceiling": FIXTURE_PACKET_CEILING if fixture_mode else LIVE_PACKET_CEILING,
        "compiler_subject": git_subject(repo_root),
        "queue": {
            "path": str(queue_resolved.relative_to(repo_root.resolve())),
            "sha256": sha256_bytes(queue_raw),
            "schema_version": queue["schema_version"],
            "subject": {
                "repository": queue_subject["repository"],
                "commit": queue_subject["commit"],
                "tree": queue_subject["tree"],
                "rollback_commit": queue_subject["rollback_commit"],
            },
            "current_active_item": queue["current"]["active_item"],
            "item_count": len(items),
        },
        "receipts": receipt_entries,
        "aggregate": {
            "state": aggregate_state,
            "admitted_item_count": len(receipt_entries),
            "pass_count": sum(entry["verdict"] == "PASS" for entry in receipt_entries),
            "fail_count": sum(entry["verdict"] == "FAIL" for entry in receipt_entries),
            "next_item": next_item,
            "queue_mutated": False,
            "queue_advanced": False,
            "compiler_physical_runtime_executed": False,
        },
        "forbidden_promotions": [
            "packet PASS to local command re-execution",
            "packet existence to raw receipt independent reproduction",
            "receipt projection to production infrastructure or user adoption",
            "local DRILL to production incident history",
            "local receipt to employment or people-management tenure",
            "compiler output to unattended queue advancement, merge, release or issue closure",
        ],
    }
    assert_public_safe(packet, canonical_bytes(packet).decode("utf-8"), label="public packet")
    return packet


def resolve_live_path(repo_root: Path, value: str, *, fixture_mode: bool) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    resolved = path.resolve()
    if not fixture_mode and not is_within(resolved, repo_root.resolve()):
        raise ValueError("live output must remain inside the repository")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate exact Local Handoff receipts and compile a minimal "
            "public-safe projection without advancing the queue."
        )
    )
    parser.add_argument("--queue", default="handoff/local-handoff-queue.json")
    parser.add_argument(
        "--receipt-root",
        action="append",
        default=[],
        help=(
            "Admitted root containing receipt files. Repeatable. "
            "Relative roots are resolved from the repository."
        ),
    )
    parser.add_argument("--receipt", action="append", default=[], metavar="ITEM_ID=PATH")
    parser.add_argument("--output", default="evidence/local-handoff/public-receipt-packet.json")
    parser.add_argument("--max-receipt-bytes", type=int, default=DEFAULT_MAX_RECEIPT_BYTES)
    parser.add_argument("--fixture-mode", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    try:
        assignments = parse_receipt_assignments(args.receipt)
        roots = [
            Path(value).resolve() if Path(value).is_absolute() else (repo_root / value).resolve()
            for value in args.receipt_root
        ] or [repo_root.resolve()]
        packet = compile_packet(
            repo_root=repo_root,
            queue_path=resolve_live_path(repo_root, args.queue, fixture_mode=False),
            receipt_roots=roots,
            receipt_assignments=assignments,
            max_receipt_bytes=args.max_receipt_bytes,
            fixture_mode=args.fixture_mode,
        )
        output = resolve_live_path(repo_root, args.output, fixture_mode=args.fixture_mode)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical_bytes(packet))
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
