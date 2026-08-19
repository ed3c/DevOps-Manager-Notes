#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib import error, request


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def http_text(url: str, timeout: float = 2.0) -> str:
    with request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8")


def wait_live(url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            if json.loads(http_text(url)).get("status") == "alive":
                return
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"demo service did not become live: {last_error}")


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema_version") != "full-manager-mvp/reviewer-inputs/v2":
        raise ValueError("unexpected reviewer input schema")
    if manifest.get("issue") != 9:
        raise ValueError("convergence manifest must target issue #9")

    receipt_inputs = manifest.get("receipt_inputs", [])
    expected_issues = {3, 4, 7, 10, 5}
    if {item.get("issue") for item in receipt_inputs} != expected_issues:
        raise ValueError("reviewer receipt inputs must bind #3/#4/#7/#10/#5 exactly")
    byte_inputs = manifest.get("byte_inputs", [])
    if len(byte_inputs) != 1 or byte_inputs[0].get("issue") != 8:
        raise ValueError("Demo Console #8 must be the only unmerged byte side input")

    for item in [manifest["git_base"], *byte_inputs, *receipt_inputs]:
        current_head = item.get("current_head")
        evidence_head = item.get("evidence_head")
        for label, head in (("current_head", current_head), ("evidence_head", evidence_head)):
            if head and not re.fullmatch(r"[0-9a-f]{40}", head):
                raise ValueError(f"invalid {label}: {head}")
        if item.get("artifact_id") and not evidence_head:
            raise ValueError("artifact-bearing input must bind an evidence_head")
        digest = item.get("artifact_digest")
        if digest and not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            raise ValueError(f"invalid artifact digest: {digest}")

    forbidden_promotions = {
        "live_kind_kubernetes": "NOT_EXERCISED",
        "real_argo_cd_reconcile": "NOT_EXERCISED",
        "load_1000_vu": "NOT_EXERCISED",
        "local_qwen_llama_cpp": "NOT_EXERCISED",
        "live_argo_rollouts_canary": "NOT_EXERCISED",
        "production_incident_history": "NOT_EXERCISED",
    }
    residuals = manifest.get("residuals", {})
    for key, expected in forbidden_promotions.items():
        if residuals.get(key) != expected:
            raise ValueError(f"residual {key} must remain {expected}")


def git_head(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="evidence/receipts/convergence/public-inputs.json",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--console-dist", default="demo-console/dist")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    manifest_path = repo_root / args.manifest
    output_dir = (repo_root / args.output_dir).resolve()
    console_dist = (repo_root / args.console_dist).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)

    if not (console_dist / "index.html").is_file():
        raise RuntimeError("Demo Console dist/index.html is missing")
    evidence_index = console_dist / "evidence-index.json"
    if not evidence_index.is_file():
        raise RuntimeError("Demo Console evidence-index.json is missing")
    evidence_text = evidence_index.read_text(encoding="utf-8")
    if "UI state cannot promote backend evidence state" not in evidence_text:
        raise RuntimeError("Demo Console public evidence boundary is missing")

    source_commit = os.getenv("REVIEWER_SOURCE_COMMIT", git_head(repo_root))
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("reviewer source commit must be an exact SHA")

    db_path = output_dir / "reviewer-demo.db"
    service_log = (output_dir / "service.log").open("w", encoding="utf-8")
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    service = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "manager_demo.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "18010",
        ],
        cwd=repo_root,
        env=env,
        stdout=service_log,
        stderr=subprocess.STDOUT,
    )

    try:
        wait_live("http://127.0.0.1:18010/health/live")
        failure_json = output_dir / "failure-drills.json"
        failure_md = output_dir / "failure-drills.md"
        subprocess.run(
            [
                sys.executable,
                "tests/failure/scenarios/run_failure_drills.py",
                "--base-url",
                "http://127.0.0.1:18010",
                "--source-commit",
                source_commit,
                "--side-inputs",
                "evidence/receipts/failure/public-m2-side-inputs.json",
                "--output",
                str(failure_json),
                "--markdown",
                str(failure_md),
            ],
            cwd=repo_root,
            check=True,
            timeout=30,
        )

        report = json.loads(failure_json.read_text(encoding="utf-8"))
        scenarios = report.get("scenarios", [])
        if report.get("verdict") != "PASS" or len(scenarios) != 7:
            raise RuntimeError("failure convergence did not preserve seven PASS drills")
        required_timeline = {
            "trigger",
            "detection",
            "mitigation",
            "recovery",
            "postmortem",
            "corrective_change",
            "same_failure_retest",
        }
        for scenario in scenarios:
            if scenario.get("classification") != "DRILL" or scenario.get("verdict") != "PASS":
                raise RuntimeError("all convergence scenarios must remain DRILL/PASS")
            timeline = scenario.get("timeline", {})
            if not required_timeline.issubset(timeline) or not all(timeline[key] for key in required_timeline):
                raise RuntimeError("failure timeline is incomplete")

        metrics = http_text("http://127.0.0.1:18010/metrics")
        (output_dir / "metrics.txt").write_text(metrics, encoding="utf-8")
        if 'manager_demo_business_oracle_total{verdict="FAIL"}' not in metrics:
            raise RuntimeError("business FAIL metric missing")
        if 'manager_demo_business_oracle_total{verdict="PASS"}' not in metrics:
            raise RuntimeError("business PASS metric missing")

        receipt = {
            "schema_version": "full-manager-mvp/reviewer-demo-evidence/v1",
            "source_commit": source_commit,
            "input_manifest_sha256": sha256_file(manifest_path),
            "console_evidence_index_sha256": sha256_file(evidence_index),
            "failure_drills_sha256": sha256_file(failure_json),
            "checks": {
                "exact_input_manifest_shape": "PASS",
                "current_vs_evidence_head_separated": "PASS",
                "demo_console_build_present": "PASS",
                "ui_evidence_promotion_guard": "PASS",
                "seven_failure_drills": "PASS",
                "complete_incident_timelines": "PASS",
                "same_failure_retest": "PASS",
                "business_pass_fail_metrics_visible": "PASS",
                "paid_api_required": "NO",
                "live_kind_kubernetes": "NOT_EXERCISED",
                "real_argo_cd_reconcile": "NOT_EXERCISED",
                "load_1000_vu": "NOT_EXERCISED",
                "local_qwen_llama_cpp": "NOT_EXERCISED",
                "live_argo_rollouts_canary": "NOT_EXERCISED",
                "production_incident_history": "NOT_EXERCISED",
            },
            "residuals": manifest["residuals"],
            "authority": manifest["authority"],
            "verdict": "PASS_BOUNDED",
            "evidence_ceiling": "GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY",
        }
        (output_dir / "reviewer-demo-receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return 0
    finally:
        service.terminate()
        try:
            service.wait(timeout=3)
        except subprocess.TimeoutExpired:
            service.kill()
            service.wait(timeout=3)
        service_log.close()
        if db_path.exists():
            db_path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
