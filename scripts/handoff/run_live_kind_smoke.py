#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Any, TextIO
from urllib import error, request

SCHEMA = "full-manager-mvp/local-kind-substrate-receipt/v1"
EVIDENCE_CEILING = "LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY"
IMAGE_TAG = "docker.io/library/manager-demo:m5-local"
NAMESPACE = "manager-demo"
DEPLOYMENT = "manager-demo"
SERVICE = "manager-demo"


def run(
    argv: list[str],
    *,
    cwd: Path,
    timeout: int,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=check,
    )


def exact_sha(value: str) -> bool:
    return re.fullmatch(r"[0-9a-f]{40}", value) is not None


def digest_ref(value: str) -> bool:
    return re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", value) is not None


def safe_cluster_name(value: str) -> str:
    if not re.fullmatch(r"manager-demo-[a-z0-9-]{1,32}", value):
        raise ValueError(
            "cluster name must match manager-demo-[a-z0-9-]{1,32}; "
            "the runner refuses arbitrary cluster names"
        )
    return value


def safe_port(value: int) -> int:
    if value < 1024 or value > 65535:
        raise ValueError("local port must be between 1024 and 65535")
    return value


def assert_port_free(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError as exc:
            raise RuntimeError(f"local port {port} is already in use") from exc


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"required local tool is missing: {name}")
    return path


def tool_version(argv: list[str], cwd: Path) -> str:
    completed = run(argv, cwd=cwd, timeout=20)
    return completed.stdout.strip()[:4000]


def git_subject(repo_root: Path) -> tuple[str, str]:
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, timeout=10).stdout.strip()
    if not exact_sha(commit) or not exact_sha(tree):
        raise RuntimeError("repository subject is not an exact git commit/tree")
    return commit, tree


def current_kubectl_context(repo_root: Path) -> str | None:
    completed = run(
        ["kubectl", "config", "current-context"],
        cwd=repo_root,
        timeout=10,
        check=False,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def oci_descriptor(archive: Path) -> dict[str, Any]:
    with tarfile.open(archive, mode="r:*") as tar:
        member = tar.getmember("index.json")
        handle = tar.extractfile(member)
        if handle is None:
            raise RuntimeError("OCI archive index.json is unreadable")
        index = json.load(handle)
    manifests = index.get("manifests", [])
    if len(manifests) != 1:
        raise RuntimeError(f"expected exactly one OCI top-level descriptor, got {len(manifests)}")
    descriptor = manifests[0]
    digest = descriptor.get("digest", "")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise RuntimeError("OCI descriptor digest is not sha256:<64 hex>")
    return descriptor


def wait_http_json(url: str, *, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with request.urlopen(url, timeout=2) as response:
                return json.load(response)
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
        time.sleep(0.25)
    raise RuntimeError(f"HTTP probe did not become ready: {url}: {last}")


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=5) as response:
        return json.load(response)


def plan(cluster_name: str, kind_node_image: str, local_port: int) -> dict[str, Any]:
    safe_cluster_name(cluster_name)
    safe_port(local_port)
    if not digest_ref(kind_node_image):
        raise ValueError("--kind-node-image must be an exact name@sha256:<64 hex> reference")
    return {
        "schema_version": "full-manager-mvp/local-kind-plan/v1",
        "cluster_name": cluster_name,
        "kind_node_image": kind_node_image,
        "local_port": local_port,
        "resource_budget": {
            "max_clusters_created": 1,
            "deployment_replicas": 2,
            "pod_cpu_request": "100m",
            "pod_cpu_limit": "1",
            "pod_memory_request": "128Mi",
            "pod_memory_limit": "512Mi",
            "handoff_timeout_seconds": 900,
            "individual_operation_timeouts_are_bounded": True,
        },
        "operations": [
            "capture the caller kubectl context",
            "refuse if the target kind cluster already exists",
            "build one OCI archive from platform/app using the pinned Dockerfile base image",
            "create one kind cluster from the exact --kind-node-image digest",
            "load the OCI archive into that cluster",
            "deploy the app by exact OCI digest with bounded Kubernetes resources",
            "probe liveness/readiness plus business PASS and forced business FAIL",
            "capture pod image IDs and exact tool/runtime subjects",
            "delete the attempted manager-demo-* cluster and temporary files in finally",
            "restore the caller kubectl context when one existed",
        ],
        "forbidden_promotions": [
            "plan-only PASS to local execution PASS",
            "local kind PASS to production Kubernetes experience",
            "local kind PASS to Argo CD or Argo Rollouts runtime PASS",
            "local kind PASS to local Qwen or llama.cpp runtime PASS",
            "local kind PASS to 1000-VU capacity/recovery PASS",
            "DRILL or local failure test to production incident history",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bounded Local Handoff runner for the first live kind/Kubernetes substrate proof."
    )
    parser.add_argument("--output", default="evidence/local-kind/local-kind-receipt.json")
    parser.add_argument("--cluster-name", default="manager-demo-m5")
    parser.add_argument("--kind-node-image", required=True)
    parser.add_argument("--local-port", type=int, default=18030)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    cluster_name = safe_cluster_name(args.cluster_name)
    local_port = safe_port(args.local_port)
    execution_plan = plan(cluster_name, args.kind_node_image, local_port)
    if args.plan_only:
        print(json.dumps(execution_plan, indent=2, sort_keys=True))
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    output = (repo_root / args.output).resolve()
    if repo_root not in output.parents:
        raise RuntimeError("--output must remain inside the repository working tree")

    started = time.monotonic()
    receipt: dict[str, Any] = {
        "schema_version": SCHEMA,
        "verdict": "FAIL",
        "evidence_ceiling": EVIDENCE_CEILING,
        "plan": execution_plan,
        "checks": {
            "local_kind_cluster_created": "NOT_EXERCISED",
            "oci_digest_bound": "NOT_EXERCISED",
            "deployment_ready": "NOT_EXERCISED",
            "business_oracle_pass": "NOT_EXERCISED",
            "business_oracle_forced_fail_visible": "NOT_EXERCISED",
            "pod_image_ids_captured": "NOT_EXERCISED",
            "cleanup": "NOT_EXERCISED",
            "kubectl_context_restored": "NOT_EXERCISED",
            "real_argo_cd_reconcile": "NOT_EXERCISED",
            "live_argo_rollouts_canary": "NOT_EXERCISED",
            "local_qwen_llama_cpp": "NOT_EXERCISED",
            "load_1000_vu": "NOT_EXERCISED",
            "production_incident_history": "NOT_EXERCISED",
        },
        "residuals": {
            "real_argo_cd_reconcile": "NOT_EXERCISED",
            "live_argo_rollouts_canary": "NOT_EXERCISED",
            "local_qwen_llama_cpp": "NOT_EXERCISED",
            "load_1000_vu": "NOT_EXERCISED",
            "registry_stored_image_signing": "NOT_EXERCISED",
            "production_users_adoption": "OUTSIDE_REPOSITORY_PROOF",
            "people_management_tenure": "OUTSIDE_REPOSITORY_PROOF",
        },
    }

    port_forward: subprocess.Popen[str] | None = None
    port_log: TextIO | None = None
    cluster_attempted = False
    temp_dir: Path | None = None
    previous_context: str | None = None
    try:
        for tool in ("git", "docker", "kind", "kubectl", "python3"):
            require_tool(tool)
        run(["docker", "info"], cwd=repo_root, timeout=30)
        run(["docker", "buildx", "version"], cwd=repo_root, timeout=20)
        assert_port_free(local_port)

        commit, tree = git_subject(repo_root)
        previous_context = current_kubectl_context(repo_root)
        receipt["subject"] = {
            "repository": "ed3c/DevOps-Manager-Notes",
            "commit": commit,
            "tree": tree,
        }
        receipt["kubectl_context_before"] = previous_context
        receipt["tool_versions"] = {
            "docker": tool_version(["docker", "version", "--format", "{{.Client.Version}}"], repo_root),
            "buildx": tool_version(["docker", "buildx", "version"], repo_root),
            "kind": tool_version(["kind", "version"], repo_root),
            "kubectl_client": tool_version(
                ["kubectl", "version", "--client", "--output=json"], repo_root
            ),
        }

        clusters = run(["kind", "get", "clusters"], cwd=repo_root, timeout=20).stdout.split()
        if cluster_name in clusters:
            raise RuntimeError(
                f"refusing to take over existing kind cluster {cluster_name}; "
                "choose a new manager-demo-* name"
            )

        temp_dir = Path(tempfile.mkdtemp(prefix="manager-demo-m5-"))
        oci_archive = temp_dir / "manager-demo.oci.tar"
        render_path = temp_dir / "deployment.yaml"

        build = run(
            [
                "docker",
                "buildx",
                "build",
                "--provenance=false",
                "--tag",
                IMAGE_TAG,
                "--output",
                f"type=oci,dest={oci_archive}",
                "-f",
                "platform/docker/Dockerfile",
                "platform/app",
            ],
            cwd=repo_root,
            timeout=300,
        )
        receipt["build_log_tail"] = build.stdout[-4000:]
        descriptor = oci_descriptor(oci_archive)
        image_digest = descriptor["digest"]
        immutable_image = f"{IMAGE_TAG}@{image_digest}"
        receipt["oci"] = {
            "tag": IMAGE_TAG,
            "descriptor_digest": image_digest,
            "immutable_image_ref": immutable_image,
            "media_type": descriptor.get("mediaType"),
        }
        receipt["checks"]["oci_digest_bound"] = "PASS"

        cluster_attempted = True
        run(
            [
                "kind",
                "create",
                "cluster",
                "--name",
                cluster_name,
                "--image",
                args.kind_node_image,
                "--wait",
                "120s",
            ],
            cwd=repo_root,
            timeout=180,
        )
        receipt["checks"]["local_kind_cluster_created"] = "PASS"

        run(
            ["kind", "load", "image-archive", str(oci_archive), "--name", cluster_name],
            cwd=repo_root,
            timeout=120,
        )
        run(
            [
                "python3",
                "platform/kubernetes/render_deployment.py",
                "--image-ref",
                immutable_image,
                "--output",
                str(render_path),
            ],
            cwd=repo_root,
            timeout=20,
        )
        run(
            ["kubectl", "apply", "-f", "platform/kubernetes/namespace.yaml"],
            cwd=repo_root,
            timeout=30,
        )
        secret_yaml = run(
            [
                "kubectl",
                "-n",
                NAMESPACE,
                "create",
                "secret",
                "generic",
                "manager-demo-db",
                "--from-literal=database-url=sqlite+pysqlite:////tmp/manager-demo.db",
                "--dry-run=client",
                "-o",
                "yaml",
            ],
            cwd=repo_root,
            timeout=20,
        ).stdout
        run(
            ["kubectl", "apply", "-f", "-"],
            cwd=repo_root,
            timeout=30,
            input_text=secret_yaml,
        )
        run(["kubectl", "apply", "-f", str(render_path)], cwd=repo_root, timeout=30)
        run(
            ["kubectl", "apply", "-f", "platform/kubernetes/service.yaml"],
            cwd=repo_root,
            timeout=30,
        )
        run(
            [
                "kubectl",
                "-n",
                NAMESPACE,
                "rollout",
                "status",
                f"deployment/{DEPLOYMENT}",
                "--timeout=120s",
            ],
            cwd=repo_root,
            timeout=140,
        )

        deployment_json = json.loads(
            run(
                [
                    "kubectl",
                    "-n",
                    NAMESPACE,
                    "get",
                    "deployment",
                    DEPLOYMENT,
                    "-o",
                    "json",
                ],
                cwd=repo_root,
                timeout=20,
            ).stdout
        )
        if deployment_json.get("status", {}).get("readyReplicas", 0) < 2:
            raise RuntimeError("expected two ready manager-demo replicas")
        receipt["checks"]["deployment_ready"] = "PASS"

        pods_json = json.loads(
            run(
                [
                    "kubectl",
                    "-n",
                    NAMESPACE,
                    "get",
                    "pods",
                    "-l",
                    "app.kubernetes.io/name=manager-demo",
                    "-o",
                    "json",
                ],
                cwd=repo_root,
                timeout=20,
            ).stdout
        )
        image_ids: list[str] = []
        for item in pods_json.get("items", []):
            for status in item.get("status", {}).get("containerStatuses", []):
                image_id = status.get("imageID")
                if image_id:
                    image_ids.append(image_id)
        if len(image_ids) < 2 or not all("sha256:" in value for value in image_ids):
            raise RuntimeError("pod runtime image IDs are missing exact sha256 identities")
        receipt["pod_image_ids"] = sorted(set(image_ids))
        receipt["checks"]["pod_image_ids_captured"] = "PASS"
        receipt["kubernetes_server"] = tool_version(
            ["kubectl", "version", "--output=json"], repo_root
        )

        port_log = (temp_dir / "port-forward.log").open("w", encoding="utf-8")
        port_forward = subprocess.Popen(
            [
                "kubectl",
                "-n",
                NAMESPACE,
                "port-forward",
                f"service/{SERVICE}",
                f"{local_port}:80",
            ],
            cwd=repo_root,
            text=True,
            stdout=port_log,
            stderr=subprocess.STDOUT,
        )
        live = wait_http_json(
            f"http://127.0.0.1:{local_port}/health/live", timeout_seconds=15
        )
        ready = wait_http_json(
            f"http://127.0.0.1:{local_port}/health/ready", timeout_seconds=15
        )
        if live.get("status") != "alive" or ready.get("status") != "ready":
            raise RuntimeError("local kind health/readiness oracle failed")

        subject = {
            "git_commit": commit,
            "deployment_revision": immutable_image,
            "kubernetes_namespace": NAMESPACE,
        }
        pass_result = post_json(
            f"http://127.0.0.1:{local_port}/v1/oracle/evaluate",
            {
                "subject": subject,
                "expected_value": "approved",
                "observed_value": "approved",
                "force_failure": False,
            },
        )
        fail_result = post_json(
            f"http://127.0.0.1:{local_port}/v1/oracle/evaluate",
            {
                "subject": subject,
                "expected_value": "approved",
                "observed_value": "rejected",
                "force_failure": True,
            },
        )
        if (
            pass_result.get("business_ok") is not True
            or pass_result.get("evidence", {}).get("verdict") != "PASS"
        ):
            raise RuntimeError("business PASS oracle did not pass")
        if (
            fail_result.get("business_ok") is not False
            or fail_result.get("evidence", {}).get("verdict") != "FAIL"
        ):
            raise RuntimeError("forced business FAIL oracle was not visible")
        receipt["checks"]["business_oracle_pass"] = "PASS"
        receipt["checks"]["business_oracle_forced_fail_visible"] = "PASS"
        receipt["business_oracle"] = {"pass": pass_result, "forced_fail": fail_result}
        receipt["verdict"] = "PASS"
    except Exception as exc:  # receipt must preserve bounded failure evidence
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["verdict"] = "FAIL"
    finally:
        if port_forward is not None:
            port_forward.terminate()
            try:
                port_forward.wait(timeout=5)
            except subprocess.TimeoutExpired:
                port_forward.kill()
                port_forward.wait(timeout=5)
        if port_log is not None:
            port_log.close()

        cleanup_errors: list[str] = []
        if cluster_attempted:
            try:
                run(
                    ["kind", "delete", "cluster", "--name", cluster_name],
                    cwd=repo_root,
                    timeout=90,
                )
            except Exception as exc:  # cleanup evidence, not silent best effort
                cleanup_errors.append(f"cluster cleanup failed: {exc}")

        if previous_context:
            try:
                run(
                    ["kubectl", "config", "use-context", previous_context],
                    cwd=repo_root,
                    timeout=20,
                )
                receipt["checks"]["kubectl_context_restored"] = "PASS"
            except Exception as exc:
                cleanup_errors.append(f"kubectl context restore failed: {exc}")
                receipt["checks"]["kubectl_context_restored"] = "FAIL"
        else:
            receipt["checks"]["kubectl_context_restored"] = "SKIPPED_NO_PRIOR_CONTEXT"

        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)
        receipt["checks"]["cleanup"] = "PASS" if not cleanup_errors else "FAIL"
        if cleanup_errors:
            receipt["cleanup_errors"] = cleanup_errors
            receipt["verdict"] = "FAIL"
        receipt["duration_seconds"] = round(time.monotonic() - started, 3)
        write_receipt(output, receipt)

    print(
        json.dumps(
            {
                "receipt": str(output.relative_to(repo_root)),
                "verdict": receipt["verdict"],
                "ceiling": EVIDENCE_CEILING,
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
