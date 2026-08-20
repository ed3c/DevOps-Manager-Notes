#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

SCHEMA = "full-manager-mvp/local-argo-ephemeral-kind-receipt/v1"
EVIDENCE_CEILING = "LOCAL_ARGO_CONTROLLERS_READY_ONLY"
DEFAULT_CLUSTER = "manager-demo-m7-argo"


def run(argv: list[str], *, cwd: Path, timeout: int, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=check,
    )


def exact_digest_ref(value: str) -> str:
    if not re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", value):
        raise ValueError("kind node image must be exact name@sha256:<64 hex>")
    return value


def exact_sha40(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("target revision must be exact 40-hex Git SHA")
    return value


def exact_sha256(value: str) -> str:
    value = value.lower().removeprefix("sha256:")
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("manifest SHA-256 must contain exactly 64 hex characters")
    return value


def https_url(value: str) -> str:
    if not re.fullmatch(r"https://[^\s]+", value):
        raise ValueError("manifest URL must use https://")
    return value


def safe_cluster(value: str) -> str:
    if not re.fullmatch(r"manager-demo-[a-z0-9-]{1,32}", value):
        raise ValueError("cluster name must match manager-demo-[a-z0-9-]{1,32}")
    return value


def git_subject(repo_root: Path) -> dict[str, str]:
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, timeout=10).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", tree):
        raise RuntimeError("unable to bind exact repository subject")
    return {"repository": "ed3c/DevOps-Manager-Notes", "commit": commit, "tree": tree}


def current_context(repo_root: Path) -> str | None:
    probe = run(["kubectl", "config", "current-context"], cwd=repo_root, timeout=10, check=False)
    if probe.returncode != 0:
        return None
    value = probe.stdout.strip()
    return value or None


def plan(
    *,
    cluster_name: str,
    kind_node_image: str,
    target_revision: str,
    argocd_url: str,
    argocd_sha: str,
    rollouts_url: str,
    rollouts_sha: str,
) -> dict:
    safe_cluster(cluster_name)
    exact_digest_ref(kind_node_image)
    exact_sha40(target_revision)
    https_url(argocd_url)
    https_url(rollouts_url)
    exact_sha256(argocd_sha)
    exact_sha256(rollouts_sha)
    return {
        "schema_version": "full-manager-mvp/local-argo-ephemeral-kind-plan/v1",
        "cluster_name": cluster_name,
        "cluster_context": f"kind-{cluster_name}",
        "kind_node_image": kind_node_image,
        "target_revision": target_revision,
        "manifests": {
            "argocd": {"url": argocd_url, "sha256": exact_sha256(argocd_sha)},
            "argo_rollouts": {"url": rollouts_url, "sha256": exact_sha256(rollouts_sha)},
        },
        "resource_budget": {
            "max_clusters_created": 1,
            "max_manifest_downloads": 2,
            "max_manifest_bytes_each": 20_000_000,
            "outer_timeout_seconds": 900,
            "cluster_cleanup_required": True,
            "kubectl_context_restore_required": True,
        },
        "operations": [
            "refuse takeover of an existing manager-demo-* kind cluster",
            "capture caller kubectl context",
            "create one ephemeral kind cluster from an exact node-image digest",
            "invoke the exact Argo controller runner against only the new kind context",
            "require inner controller receipt PASS and cleanup PASS",
            "delete the attempted cluster and restore caller kubectl context in finally",
        ],
        "forbidden_promotions": [
            "plan-only PASS to Argo runtime PASS",
            "ephemeral kind creation to production Kubernetes experience",
            "controller readiness to Argo CD Application reconciliation PASS",
            "controller readiness to live Argo Rollouts canary PASS",
            "local Argo execution to production deployment or customer traffic",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-contained bounded Argo controller proof on an ephemeral local kind cluster.")
    parser.add_argument("--cluster-name", default=DEFAULT_CLUSTER)
    parser.add_argument("--kind-node-image", required=True)
    parser.add_argument("--target-revision", required=True)
    parser.add_argument("--argocd-manifest-url", required=True)
    parser.add_argument("--argocd-manifest-sha256", required=True)
    parser.add_argument("--rollouts-manifest-url", required=True)
    parser.add_argument("--rollouts-manifest-sha256", required=True)
    parser.add_argument("--output", default="evidence/local-argo/ephemeral-kind-receipt.json")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    execution_plan = plan(
        cluster_name=args.cluster_name,
        kind_node_image=args.kind_node_image,
        target_revision=args.target_revision,
        argocd_url=args.argocd_manifest_url,
        argocd_sha=args.argocd_manifest_sha256,
        rollouts_url=args.rollouts_manifest_url,
        rollouts_sha=args.rollouts_manifest_sha256,
    )
    if args.plan_only:
        print(json.dumps(execution_plan, indent=2, sort_keys=True))
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    output = (repo_root / args.output).resolve()
    if repo_root not in output.parents:
        raise RuntimeError("--output must remain inside repository")
    for tool in ("git", "kind", "kubectl", "python3"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"required local tool missing: {tool}")

    subject = git_subject(repo_root)
    started = time.monotonic()
    previous_context = current_context(repo_root)
    cluster_attempted = False
    cleanup_errors: list[str] = []
    inner_path = output.parent / "controller-receipt.json"
    receipt = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": subject,
        "plan": execution_plan,
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "cluster_created": "NOT_EXERCISED",
            "inner_controller_receipt_pass": "NOT_EXERCISED",
            "inner_cleanup_pass": "NOT_EXERCISED",
            "cluster_cleanup": "NOT_EXERCISED",
            "kubectl_context_restored": "NOT_EXERCISED",
            "argo_cd_application_reconcile": "NOT_EXERCISED",
            "live_argo_rollouts_canary": "NOT_EXERCISED",
            "production_deployment": "NOT_EXERCISED",
        },
    }

    try:
        existing = run(["kind", "get", "clusters"], cwd=repo_root, timeout=20).stdout.split()
        if args.cluster_name in existing:
            raise RuntimeError(f"refusing to take over existing kind cluster {args.cluster_name}")
        cluster_attempted = True
        run(
            [
                "kind", "create", "cluster",
                "--name", args.cluster_name,
                "--image", args.kind_node_image,
                "--wait", "120s",
            ],
            cwd=repo_root,
            timeout=180,
        )
        receipt["checks"]["cluster_created"] = "PASS"

        completed = run(
            [
                "python3", "scripts/handoff/run_argo_control_plane.py",
                "--cluster-context", f"kind-{args.cluster_name}",
                "--target-revision", args.target_revision,
                "--argocd-manifest-url", args.argocd_manifest_url,
                "--argocd-manifest-sha256", args.argocd_manifest_sha256,
                "--rollouts-manifest-url", args.rollouts_manifest_url,
                "--rollouts-manifest-sha256", args.rollouts_manifest_sha256,
                "--output", str(inner_path.relative_to(repo_root)),
            ],
            cwd=repo_root,
            timeout=600,
            check=False,
        )
        receipt["inner_output_tail"] = completed.stdout[-4000:]
        if completed.returncode != 0 or not inner_path.is_file():
            raise RuntimeError(f"inner Argo controller runner failed with exit {completed.returncode}")
        inner = json.loads(inner_path.read_text(encoding="utf-8"))
        if inner.get("state") != "PASS":
            raise RuntimeError("inner Argo controller receipt is not PASS")
        if inner.get("checks", {}).get("cleanup") != "PASS":
            raise RuntimeError("inner Argo controller cleanup is not PASS")
        if inner.get("evidence_ceiling") != EVIDENCE_CEILING:
            raise RuntimeError("inner Argo controller evidence ceiling drifted")
        receipt["checks"]["inner_controller_receipt_pass"] = "PASS"
        receipt["checks"]["inner_cleanup_pass"] = "PASS"
        receipt["inner_receipt"] = {
            "path": str(inner_path.relative_to(repo_root)),
            "schema_version": inner.get("schema_version"),
            "evidence_ceiling": inner.get("evidence_ceiling"),
        }
        receipt["state"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"
    finally:
        if cluster_attempted:
            result = run(["kind", "delete", "cluster", "--name", args.cluster_name], cwd=repo_root, timeout=120, check=False)
            receipt["checks"]["cluster_cleanup"] = "PASS" if result.returncode == 0 else "FAIL"
            if result.returncode != 0:
                cleanup_errors.append("failed to delete ephemeral kind cluster")
        else:
            receipt["checks"]["cluster_cleanup"] = "SKIPPED_NOT_CREATED"
        if previous_context:
            result = run(["kubectl", "config", "use-context", previous_context], cwd=repo_root, timeout=20, check=False)
            receipt["checks"]["kubectl_context_restored"] = "PASS" if result.returncode == 0 else "FAIL"
            if result.returncode != 0:
                cleanup_errors.append("failed to restore kubectl context")
        else:
            receipt["checks"]["kubectl_context_restored"] = "SKIPPED_NO_PRIOR_CONTEXT"
        if cleanup_errors:
            receipt["cleanup_errors"] = cleanup_errors
            receipt["state"] = "FAIL"
        receipt["duration_seconds"] = round(time.monotonic() - started, 3)
        write_receipt(output, receipt)

    print(json.dumps({"receipt": str(output.relative_to(repo_root)), "state": receipt["state"], "ceiling": EVIDENCE_CEILING}, sort_keys=True))
    return 0 if receipt["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
