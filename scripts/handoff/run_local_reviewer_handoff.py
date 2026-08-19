#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "full-manager-mvp/local-reviewer-handoff-receipt/v1"
EVIDENCE_CEILING = "LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_git_subject(repo_root: Path) -> tuple[str, str]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", tree):
        raise RuntimeError("unable to bind exact git commit/tree")
    return commit, tree


def ensure_repo_path(repo_root: Path, value: str) -> Path:
    path = (repo_root / value).resolve()
    if path != repo_root and repo_root not in path.parents:
        raise ValueError("output/work path must remain inside repository")
    return path


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Canonical Local Handoff wrapper for the deterministic reviewer demo.")
    parser.add_argument("--output", default="evidence/local-reviewer/handoff-receipt.json")
    parser.add_argument("--work-dir", default="evidence/local-reviewer/work")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    output = ensure_repo_path(repo_root, args.output)
    work_dir = ensure_repo_path(repo_root, args.work_dir)
    commit, tree = exact_git_subject(repo_root)

    receipt: dict = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": {
            "repository": "ed3c/DevOps-Manager-Notes",
            "commit": commit,
            "tree": tree,
        },
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "reviewer_demo_pass_bounded": "NOT_EXERCISED",
            "seven_failure_drills": "NOT_EXERCISED",
            "same_failure_retest": "NOT_EXERCISED",
            "business_pass_fail_metrics_visible": "NOT_EXERCISED",
            "paid_api_required": "NOT_EXERCISED",
            "generated_workspace_cleanup": "NOT_EXERCISED",
            "live_kind_kubernetes": "NOT_EXERCISED",
            "real_argo_cd_reconcile": "NOT_EXERCISED",
            "live_argo_rollouts_canary": "NOT_EXERCISED",
            "local_qwen_llama_cpp": "NOT_EXERCISED",
            "load_1000_vu": "NOT_EXERCISED",
            "production_incident_history": "NOT_EXERCISED",
        },
    }

    try:
        completed = subprocess.run(
            ["bash", "scripts/demo/run_reviewer_demo.sh", str(work_dir.relative_to(repo_root))],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=900,
            check=False,
        )
        receipt["command_exit_code"] = completed.returncode
        receipt["command_output_tail"] = completed.stdout[-4000:]
        if completed.returncode != 0:
            raise RuntimeError(f"reviewer demo command failed with exit {completed.returncode}")

        source_receipt = work_dir / "reviewer-demo-receipt.json"
        if not source_receipt.is_file():
            raise RuntimeError("reviewer-demo-receipt.json missing")
        source = json.loads(source_receipt.read_text(encoding="utf-8"))
        if source.get("verdict") != "PASS_BOUNDED":
            raise RuntimeError("reviewer demo did not return PASS_BOUNDED")

        required = {
            "seven_failure_drills": "PASS",
            "same_failure_retest": "PASS",
            "business_pass_fail_metrics_visible": "PASS",
            "paid_api_required": "NO",
        }
        checks = source.get("checks", {})
        for key, expected in required.items():
            if checks.get(key) != expected:
                raise RuntimeError(f"reviewer demo check {key} expected {expected}, got {checks.get(key)!r}")

        generated_paths = [
            repo_root / "demo-console" / "node_modules",
            repo_root / "demo-console" / "public",
            repo_root / "demo-console" / "dist",
        ]
        if any(path.exists() for path in generated_paths):
            raise RuntimeError("reviewer demo left generated workspace paths behind")

        receipt["source_receipt"] = {
            "path": str(source_receipt.relative_to(repo_root)),
            "sha256": sha256_file(source_receipt),
            "schema_version": source.get("schema_version"),
            "verdict": source.get("verdict"),
        }
        receipt["checks"].update(
            {
                "reviewer_demo_pass_bounded": "PASS",
                "seven_failure_drills": "PASS",
                "same_failure_retest": "PASS",
                "business_pass_fail_metrics_visible": "PASS",
                "paid_api_required": "NO",
                "generated_workspace_cleanup": "PASS",
            }
        )
        receipt["state"] = "PASS"
    except Exception as exc:  # keep failure visible in the durable handoff receipt
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"

    write_receipt(output, receipt)
    print(json.dumps({"receipt": str(output.relative_to(repo_root)), "state": receipt["state"], "ceiling": EVIDENCE_CEILING}, sort_keys=True))
    return 0 if receipt["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
