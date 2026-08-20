#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

REPO = "ed3c/DevOps-Manager-Notes"
QUEUE_SCHEMA = "agentic-tech-lead/local-handoff-queue/v1"
COMPILE_SCHEMA = "full-manager-mvp/m7-advanced-queue-compile-receipt/v1"
PREDECESSOR_COMMIT = "4cc3e162c00a3af240bab9e62482e07bb3e4f9a1"
PREDECESSOR_TREE = "5ff3349c1eb5c7976263c2e89347a353ccbc1072"
REVIEWER_SCHEMA = "full-manager-mvp/local-reviewer-handoff-receipt/v1"
REVIEWER_CEILING = "LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY"
KIND_SCHEMA = "full-manager-mvp/local-kind-substrate-receipt/v1"
KIND_CEILING = "LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_git_subject(repo_root: Path) -> tuple[str, str, str]:
    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=repo_root, text=True).strip()

    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    rollback = git("rev-parse", "HEAD^")
    for name, value in (("commit", commit), ("tree", tree), ("rollback", rollback)):
        if not re.fullmatch(r"[0-9a-f]{40}", value):
            raise RuntimeError(f"{name} is not an exact SHA-40")
    return commit, tree, rollback


def ensure_path(repo_root: Path, value: str, *, fixture_mode: bool) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    if not fixture_mode and path != repo_root and repo_root not in path.parents:
        raise ValueError("live compiler outputs must remain inside the repository")
    return path


def require_fixture_contract(receipt: dict[str, Any], *, fixture_mode: bool, label: str) -> None:
    kind = receipt.get("evidence_kind")
    if fixture_mode:
        if kind != "FIXTURE":
            raise ValueError(f"{label} receipt must declare evidence_kind=FIXTURE in fixture mode")
    elif kind == "FIXTURE":
        raise ValueError(f"{label} fixture receipt is forbidden outside --fixture-mode")


def require_subject(receipt: dict[str, Any], *, label: str) -> None:
    subject = receipt.get("subject", {})
    if subject.get("repository") != REPO:
        raise ValueError(f"{label} repository subject mismatch")
    if subject.get("commit") != PREDECESSOR_COMMIT:
        raise ValueError(f"{label} predecessor commit mismatch")
    if subject.get("tree") != PREDECESSOR_TREE:
        raise ValueError(f"{label} predecessor tree mismatch")


def admit_reviewer(receipt: dict[str, Any], *, fixture_mode: bool) -> None:
    require_fixture_contract(receipt, fixture_mode=fixture_mode, label="reviewer")
    require_subject(receipt, label="reviewer")
    if receipt.get("schema_version") != REVIEWER_SCHEMA:
        raise ValueError("reviewer receipt schema mismatch")
    if receipt.get("state") != "PASS":
        raise ValueError("reviewer receipt must be PASS")
    if receipt.get("evidence_ceiling") != REVIEWER_CEILING:
        raise ValueError("reviewer evidence ceiling mismatch")
    checks = receipt.get("checks", {})
    required = {
        "reviewer_demo_pass_bounded": "PASS",
        "seven_failure_drills": "PASS",
        "same_failure_retest": "PASS",
        "business_pass_fail_metrics_visible": "PASS",
        "generated_workspace_cleanup": "PASS",
    }
    for key, expected in required.items():
        if checks.get(key) != expected:
            raise ValueError(f"reviewer check {key} expected {expected}")


def admit_kind(receipt: dict[str, Any], *, fixture_mode: bool) -> None:
    require_fixture_contract(receipt, fixture_mode=fixture_mode, label="kind")
    require_subject(receipt, label="kind")
    if receipt.get("schema_version") != KIND_SCHEMA:
        raise ValueError("kind receipt schema mismatch")
    if receipt.get("verdict") != "PASS":
        raise ValueError("kind receipt must have verdict PASS")
    if receipt.get("evidence_ceiling") != KIND_CEILING:
        raise ValueError("kind evidence ceiling mismatch")
    checks = receipt.get("checks", {})
    required = {
        "local_kind_cluster_created": "PASS",
        "oci_digest_bound": "PASS",
        "deployment_ready": "PASS",
        "business_oracle_pass": "PASS",
        "business_oracle_forced_fail_visible": "PASS",
        "pod_image_ids_captured": "PASS",
        "cleanup": "PASS",
    }
    for key, expected in required.items():
        if checks.get(key) != expected:
            raise ValueError(f"kind check {key} expected {expected}")
    if checks.get("kubectl_context_restored") not in {"PASS", "SKIPPED_NO_PRIOR_CONTEXT"}:
        raise ValueError("kind kubectl context restoration is not admitted")


def item(
    *,
    item_id: str,
    task_ref: str,
    state: str,
    predecessor: str | None,
    subject_commit: str,
    capabilities: list[str],
    argv: list[str],
    timeout: int,
    environment_names: list[str],
    receipt_path: str,
    receipt_schema: str,
    forbidden_promotions: list[str],
    next_id: str | None,
) -> dict[str, Any]:
    return {
        "id": item_id,
        "task_ref": task_ref,
        "state": state,
        "entry": {
            "predecessor": predecessor,
            "required_subject_commit": subject_commit,
            "required_capabilities": capabilities,
        },
        "runtime_lane": {
            "class": "LOCAL_HOST",
            "commands": [
                {
                    "argv": argv,
                    "cwd": ".",
                    "timeout_seconds": timeout,
                    "environment_names": environment_names,
                }
            ],
            "unresolved_operations": [],
            "live_evidence_required": True,
        },
        "receipt": {
            "path": receipt_path,
            "schema": receipt_schema,
            "required_states": ["PASS", "FAIL"],
            "forbidden_promotions": forbidden_promotions,
        },
        "exit": {
            "requires_receipt": True,
            "required_verdict": "PASS",
            "cleanup_required": True,
        },
        "next": next_id,
    }


def compile_queue(*, commit: str, tree: str, rollback: str) -> dict[str, Any]:
    argo = "M7-ARGO-CONTROLLERS-001"
    model = "M7-LOCAL-MODEL-002"
    capacity = "M7-CAPACITY-003"
    signing = "M7-REGISTRY-SIGNING-004"
    return {
        "schema_version": QUEUE_SCHEMA,
        "subject": {
            "repository": REPO,
            "commit": commit,
            "tree": tree,
            "rollback_commit": rollback,
        },
        "authority": {
            "automation_forbidden": [
                "merge",
                "force_push",
                "issue_close",
                "queue_advance",
                "provider_activation",
                "semantic_conflict_resolution",
                "release",
                "production_promotion",
                "production_rollback_admission",
                "permission_widening",
                "repository_visibility_change",
                "real_experience_claim_promotion",
            ],
            "human_owned": [
                "merge and release admission",
                "repository visibility and permission decisions",
                "production promotion or rollback decisions",
                "semantic conflict decisions",
                "real user incident production and people-management claims",
            ],
        },
        "current": {"active_item": argo, "state": "ACTIVE"},
        "items": [
            item(
                item_id=argo,
                task_ref=f"{REPO}#60",
                state="ACTIVE",
                predecessor=None,
                subject_commit=commit,
                capabilities=["LOCAL_HOST", "git", "python3", "kind", "kubectl", "outbound HTTPS manifest reachability"],
                argv=["bash", "scripts/handoff/run_argo_ephemeral_kind_from_env.sh", "--output", "evidence/local-argo/ephemeral-kind-receipt.json"],
                timeout=900,
                environment_names=[
                    "M7_ARGO_KIND_NODE_IMAGE",
                    "M7_ARGO_TARGET_REVISION",
                    "M7_ARGO_CD_MANIFEST_URL",
                    "M7_ARGO_CD_MANIFEST_SHA256",
                    "M7_ARGO_ROLLOUTS_MANIFEST_URL",
                    "M7_ARGO_ROLLOUTS_MANIFEST_SHA256",
                ],
                receipt_path="evidence/local-argo/ephemeral-kind-receipt.json",
                receipt_schema="full-manager-mvp/local-argo-ephemeral-kind-receipt/v1",
                forbidden_promotions=[
                    "Argo controller PASS to Argo CD Application reconciliation PASS",
                    "Argo controller PASS to live Rollouts canary PASS",
                    "local Argo PASS to production deployment experience",
                ],
                next_id=model,
            ),
            item(
                item_id=model,
                task_ref=f"{REPO}#60",
                state="BLOCKED_BY_PREDECESSOR",
                predecessor=argo,
                subject_commit=commit,
                capabilities=["LOCAL_HOST", "git", "python3", "cmake", "outbound HTTPS/Git reachability"],
                argv=["bash", "scripts/handoff/run_local_model_from_env.sh", "--output", "evidence/local-model/local-model-receipt.json"],
                timeout=900,
                environment_names=["M6_LLAMA_CPP_COMMIT", "M6_MODEL_URL", "M6_MODEL_SHA256", "M6_MODEL_LICENSE_ID"],
                receipt_path="evidence/local-model/local-model-receipt.json",
                receipt_schema="full-manager-mvp/local-model-receipt/v1",
                forbidden_promotions=[
                    "local model PASS to production LLM traffic",
                    "local model PASS to production latency or adoption",
                    "model license metadata to blanket legal clearance",
                ],
                next_id=capacity,
            ),
            item(
                item_id=capacity,
                task_ref=f"{REPO}#60",
                state="BLOCKED_BY_PREDECESSOR",
                predecessor=model,
                subject_commit=commit,
                capabilities=["LOCAL_HOST", "python3", "loopback port 18040", "outbound Python package reachability"],
                argv=[
                    "python3", "scripts/handoff/run_local_capacity.py",
                    "--users", "1000",
                    "--spawn-rate", "100",
                    "--duration-seconds", "30",
                    "--p95-limit-ms", "1000",
                    "--failure-ratio-limit", "0.01",
                    "--local-port", "18040",
                    "--output", "evidence/local-capacity/local-capacity-receipt.json",
                ],
                timeout=600,
                environment_names=[],
                receipt_path="evidence/local-capacity/local-capacity-receipt.json",
                receipt_schema="full-manager-mvp/local-capacity-receipt/v1",
                forbidden_promotions=[
                    "1000 virtual users to 1000 real users",
                    "local synthetic load PASS to production capacity or adoption",
                    "local p95 to production SLO attainment",
                ],
                next_id=signing,
            ),
            item(
                item_id=signing,
                task_ref=f"{REPO}#60",
                state="BLOCKED_BY_PREDECESSOR",
                predecessor=capacity,
                subject_commit=commit,
                capabilities=["LOCAL_HOST", "git", "docker daemon", "exact local cosign binary"],
                argv=["bash", "scripts/handoff/run_local_registry_signing_from_env.sh", "--output", "evidence/local-registry-signing/receipt.json"],
                timeout=900,
                environment_names=["M6_REGISTRY_IMAGE", "M6_COSIGN_BIN", "M6_COSIGN_SHA256"],
                receipt_path="evidence/local-registry-signing/receipt.json",
                receipt_schema="full-manager-mvp/local-registry-signing-receipt/v1",
                forbidden_promotions=[
                    "local registry signature PASS to production key custody",
                    "loopback registry PASS to external registry credential readiness",
                    "local signature verification to organization-wide supply-chain compliance",
                ],
                next_id=None,
            ),
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the M7 advanced canonical Local Handoff epoch after admitted M5 predecessor receipts.")
    parser.add_argument("--reviewer-receipt", default="evidence/local-reviewer/handoff-receipt.json")
    parser.add_argument("--kind-receipt", default="evidence/local-kind/local-kind-receipt.json")
    parser.add_argument("--output", default="handoff/m7-advanced-local-handoff-queue.json")
    parser.add_argument("--compile-receipt", default="evidence/receipts/handoff/m7-advanced-queue-compile-receipt.json")
    parser.add_argument("--fixture-mode", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    reviewer_path = Path(args.reviewer_receipt).resolve() if Path(args.reviewer_receipt).is_absolute() else (repo_root / args.reviewer_receipt).resolve()
    kind_path = Path(args.kind_receipt).resolve() if Path(args.kind_receipt).is_absolute() else (repo_root / args.kind_receipt).resolve()
    if not reviewer_path.is_file() or not kind_path.is_file():
        raise SystemExit("required predecessor receipt is absent")

    reviewer = load_json(reviewer_path)
    kind = load_json(kind_path)
    admit_reviewer(reviewer, fixture_mode=args.fixture_mode)
    admit_kind(kind, fixture_mode=args.fixture_mode)

    commit, tree, rollback = exact_git_subject(repo_root)
    queue = compile_queue(commit=commit, tree=tree, rollback=rollback)
    output = ensure_path(repo_root, args.output, fixture_mode=args.fixture_mode)
    compile_receipt = ensure_path(repo_root, args.compile_receipt, fixture_mode=args.fixture_mode)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(queue, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema_version": COMPILE_SCHEMA,
        "state": "PASS",
        "evidence_kind": "FIXTURE" if args.fixture_mode else "LIVE_PREDECESSOR_INPUTS",
        "subject": {"repository": REPO, "commit": commit, "tree": tree},
        "predecessor_epoch": {"commit": PREDECESSOR_COMMIT, "tree": PREDECESSOR_TREE},
        "predecessor_receipts": {
            "reviewer_sha256": sha256_file(reviewer_path),
            "kind_sha256": sha256_file(kind_path),
        },
        "queue": {"path": str(output), "sha256": sha256_file(output), "active_item": queue["current"]["active_item"]},
        "evidence_ceiling": "FIXTURE_COMPILER_CONTRACT_ONLY" if args.fixture_mode else "LOCAL_HANDOFF_QUEUE_COMPILATION_ONLY",
        "physical_runtime_executed": False,
    }
    compile_receipt.parent.mkdir(parents=True, exist_ok=True)
    compile_receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"queue": str(output), "compile_receipt": str(compile_receipt), "state": "PASS", "fixture_mode": args.fixture_mode}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
