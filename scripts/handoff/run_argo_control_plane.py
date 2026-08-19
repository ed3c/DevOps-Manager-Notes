#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from urllib import request

SCHEMA = "full-manager-mvp/local-argo-control-plane-receipt/v1"
EVIDENCE_CEILING = "LOCAL_ARGO_CONTROLLERS_READY_ONLY"


def exact_sha256(value: str) -> str:
    value = value.lower().removeprefix("sha256:")
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("artifact SHA-256 must contain exactly 64 hex characters")
    return value


def https_url(value: str) -> str:
    if not re.fullmatch(r"https://[^\s]+", value):
        raise ValueError("manifest URL must use https://")
    return value


def context_name(value: str) -> str:
    if not re.fullmatch(r"kind-manager-demo-[a-z0-9-]{1,40}", value):
        raise ValueError("cluster context must match kind-manager-demo-[a-z0-9-]{1,40}")
    return value


def exact_sha40(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("target revision must be an exact 40-hex Git SHA")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def kubectl(context: str, args: list[str], *, cwd: Path, timeout: int, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["kubectl", "--context", context, *args], cwd=cwd, timeout=timeout, check=check)


def git_subject(repo_root: Path) -> dict[str, str]:
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, timeout=10).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", tree):
        raise RuntimeError("unable to bind exact repository subject")
    return {"repository": "ed3c/DevOps-Manager-Notes", "commit": commit, "tree": tree}


def plan(*, cluster_context: str, target_revision: str, argocd_url: str, argocd_sha: str, rollouts_url: str, rollouts_sha: str) -> dict:
    context_name(cluster_context)
    exact_sha40(target_revision)
    https_url(argocd_url)
    https_url(rollouts_url)
    exact_sha256(argocd_sha)
    exact_sha256(rollouts_sha)
    return {
        "schema_version": "full-manager-mvp/local-argo-control-plane-plan/v1",
        "cluster_context": cluster_context,
        "target_revision": target_revision,
        "artifacts": {
            "argocd": {"url": argocd_url, "sha256": exact_sha256(argocd_sha)},
            "argo_rollouts": {"url": rollouts_url, "sha256": exact_sha256(rollouts_sha)},
        },
        "resource_budget": {
            "max_target_clusters": 1,
            "namespaces": ["argocd", "argo-rollouts"],
            "install_timeout_seconds": 240,
            "cleanup_timeout_seconds": 180,
            "max_manifest_downloads": 2,
        },
        "operations": [
            "refuse non manager-demo kind contexts and pre-existing argocd/argo-rollouts namespaces",
            "download exactly two HTTPS install manifests and verify SHA-256 before apply",
            "create both runner-owned namespaces and apply each manifest with an explicit namespace through the named local kind context",
            "wait for controller deployments and verify Application/Rollout CRDs",
            "record exact manifest digests, Git subject and Kubernetes server identity",
            "delete applied manifests and only runner-owned namespaces in finally after the context is admitted",
        ],
        "forbidden_promotions": [
            "plan-only PASS to Argo runtime PASS",
            "controller readiness to Argo CD application reconciliation PASS",
            "controller readiness to Argo Rollouts canary analysis PASS",
            "local Argo runtime to production deployment experience",
            "local control-plane execution to real customer traffic or people-management tenure",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bounded Argo CD/Rollouts controller installation proof on an isolated local kind cluster."
    )
    parser.add_argument("--cluster-context", required=True)
    parser.add_argument("--target-revision", required=True)
    parser.add_argument("--argocd-manifest-url", required=True)
    parser.add_argument("--argocd-manifest-sha256", required=True)
    parser.add_argument("--rollouts-manifest-url", required=True)
    parser.add_argument("--rollouts-manifest-sha256", required=True)
    parser.add_argument("--output", default="evidence/local-argo/local-argo-control-plane-receipt.json")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    execution_plan = plan(
        cluster_context=args.cluster_context,
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
    if shutil.which("kubectl") is None or shutil.which("git") is None:
        raise RuntimeError("git and kubectl are required")

    receipt = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": git_subject(repo_root),
        "plan": execution_plan,
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "argocd_manifest_sha256_verified": "NOT_EXERCISED",
            "rollouts_manifest_sha256_verified": "NOT_EXERCISED",
            "argocd_namespace_owned": "NOT_EXERCISED",
            "rollouts_namespace_owned": "NOT_EXERCISED",
            "argocd_controllers_available": "NOT_EXERCISED",
            "rollouts_controller_available": "NOT_EXERCISED",
            "application_crd_present": "NOT_EXERCISED",
            "rollout_crd_present": "NOT_EXERCISED",
            "cleanup": "NOT_EXERCISED",
            "real_argo_cd_reconcile": "NOT_EXERCISED",
            "live_argo_rollouts_canary": "NOT_EXERCISED",
            "production_deployment": "NOT_EXERCISED",
        },
    }
    started = time.monotonic()
    temp_root: Path | None = None
    context_admitted = False
    argocd_namespace_created = False
    rollouts_namespace_created = False
    argocd_applied = False
    rollouts_applied = False
    cleanup_errors: list[str] = []
    try:
        contexts = run(["kubectl", "config", "get-contexts", "-o", "name"], cwd=repo_root, timeout=20).stdout.split()
        if args.cluster_context not in contexts:
            raise RuntimeError("required local kind context does not exist")
        context_admitted = True

        for namespace in ("argocd", "argo-rollouts"):
            probe = kubectl(
                args.cluster_context,
                ["get", "namespace", namespace],
                cwd=repo_root,
                timeout=20,
                check=False,
            )
            if probe.returncode == 0:
                raise RuntimeError(f"refusing to take over pre-existing namespace {namespace}")

        temp_root = Path(tempfile.mkdtemp(prefix="manager-demo-m6-argo-"))
        argocd_file = temp_root / "argocd-install.yaml"
        rollouts_file = temp_root / "argo-rollouts-install.yaml"
        for url, destination in (
            (args.argocd_manifest_url, argocd_file),
            (args.rollouts_manifest_url, rollouts_file),
        ):
            with request.urlopen(url, timeout=30) as response, destination.open("wb") as handle:
                shutil.copyfileobj(response, handle, length=1024 * 1024)

        if sha256_file(argocd_file) != exact_sha256(args.argocd_manifest_sha256):
            raise RuntimeError("Argo CD manifest SHA-256 mismatch")
        receipt["checks"]["argocd_manifest_sha256_verified"] = "PASS"
        if sha256_file(rollouts_file) != exact_sha256(args.rollouts_manifest_sha256):
            raise RuntimeError("Argo Rollouts manifest SHA-256 mismatch")
        receipt["checks"]["rollouts_manifest_sha256_verified"] = "PASS"

        kubectl(args.cluster_context, ["create", "namespace", "argocd"], cwd=repo_root, timeout=30)
        argocd_namespace_created = True
        receipt["checks"]["argocd_namespace_owned"] = "PASS"
        kubectl(args.cluster_context, ["create", "namespace", "argo-rollouts"], cwd=repo_root, timeout=30)
        rollouts_namespace_created = True
        receipt["checks"]["rollouts_namespace_owned"] = "PASS"

        kubectl(
            args.cluster_context,
            ["apply", "-n", "argocd", "-f", str(argocd_file)],
            cwd=repo_root,
            timeout=120,
        )
        argocd_applied = True
        kubectl(
            args.cluster_context,
            ["apply", "-n", "argo-rollouts", "-f", str(rollouts_file)],
            cwd=repo_root,
            timeout=120,
        )
        rollouts_applied = True

        kubectl(
            args.cluster_context,
            ["wait", "--for=condition=Available", "deployment", "--all", "-n", "argocd", "--timeout=180s"],
            cwd=repo_root,
            timeout=200,
        )
        receipt["checks"]["argocd_controllers_available"] = "PASS"
        kubectl(
            args.cluster_context,
            ["wait", "--for=condition=Available", "deployment", "--all", "-n", "argo-rollouts", "--timeout=180s"],
            cwd=repo_root,
            timeout=200,
        )
        receipt["checks"]["rollouts_controller_available"] = "PASS"
        kubectl(args.cluster_context, ["get", "crd", "applications.argoproj.io"], cwd=repo_root, timeout=20)
        receipt["checks"]["application_crd_present"] = "PASS"
        kubectl(args.cluster_context, ["get", "crd", "rollouts.argoproj.io"], cwd=repo_root, timeout=20)
        receipt["checks"]["rollout_crd_present"] = "PASS"
        receipt["kubernetes_version"] = kubectl(
            args.cluster_context,
            ["version", "-o", "json"],
            cwd=repo_root,
            timeout=20,
        ).stdout[:4000]
        receipt["manifest_subjects"] = {
            "argocd_sha256": sha256_file(argocd_file),
            "rollouts_sha256": sha256_file(rollouts_file),
            "target_revision": args.target_revision,
        }
        receipt["state"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"
    finally:
        if context_admitted and rollouts_applied and temp_root is not None:
            result = kubectl(
                args.cluster_context,
                ["delete", "-n", "argo-rollouts", "-f", str(temp_root / "argo-rollouts-install.yaml"), "--ignore-not-found=true", "--wait=false"],
                cwd=repo_root,
                timeout=120,
                check=False,
            )
            if result.returncode != 0:
                cleanup_errors.append("failed to delete Argo Rollouts manifest")
        if context_admitted and argocd_applied and temp_root is not None:
            result = kubectl(
                args.cluster_context,
                ["delete", "-n", "argocd", "-f", str(temp_root / "argocd-install.yaml"), "--ignore-not-found=true", "--wait=false"],
                cwd=repo_root,
                timeout=120,
                check=False,
            )
            if result.returncode != 0:
                cleanup_errors.append("failed to delete Argo CD manifest")
        if context_admitted and rollouts_namespace_created:
            result = kubectl(
                args.cluster_context,
                ["delete", "namespace", "argo-rollouts", "--ignore-not-found=true", "--wait=false"],
                cwd=repo_root,
                timeout=60,
                check=False,
            )
            if result.returncode != 0:
                cleanup_errors.append("failed to delete namespace argo-rollouts")
        if context_admitted and argocd_namespace_created:
            result = kubectl(
                args.cluster_context,
                ["delete", "namespace", "argocd", "--ignore-not-found=true", "--wait=false"],
                cwd=repo_root,
                timeout=60,
                check=False,
            )
            if result.returncode != 0:
                cleanup_errors.append("failed to delete namespace argocd")
        if temp_root is not None:
            shutil.rmtree(temp_root, ignore_errors=True)
        receipt["checks"]["cleanup"] = "PASS" if not cleanup_errors else "FAIL"
        if cleanup_errors:
            receipt["cleanup_errors"] = cleanup_errors
            receipt["state"] = "FAIL"
        receipt["duration_seconds"] = round(time.monotonic() - started, 3)
        write_receipt(output, receipt)

    print(
        json.dumps(
            {"receipt": str(output.relative_to(repo_root)), "state": receipt["state"], "ceiling": EVIDENCE_CEILING},
            sort_keys=True,
        )
    )
    return 0 if receipt["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
