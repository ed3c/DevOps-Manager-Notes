#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path

SCHEMA = "full-manager-mvp/local-registry-signing-receipt/v1"
EVIDENCE_CEILING = "LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY"


def exact_image_ref(value: str) -> str:
    if not re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", value):
        raise ValueError("registry image must be an exact name@sha256:<64 hex> reference")
    return value


def exact_sha256(value: str) -> str:
    value = value.lower().removeprefix("sha256:")
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("cosign binary SHA-256 must contain exactly 64 hex characters")
    return value


def safe_port(value: int) -> int:
    if value < 1024 or value > 65535:
        raise ValueError("registry port must be between 1024 and 65535")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(argv: list[str], *, cwd: Path, timeout: int, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=check,
    )


def git_subject(repo_root: Path) -> dict[str, str]:
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, timeout=10).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", tree):
        raise RuntimeError("unable to bind exact repository subject")
    return {"repository": "ed3c/DevOps-Manager-Notes", "commit": commit, "tree": tree}


def assert_port_free(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError as exc:
            raise RuntimeError(f"registry port {port} is already in use") from exc


def plan(*, registry_image: str, cosign_bin: str, cosign_sha256: str, registry_port: int) -> dict:
    exact_image_ref(registry_image)
    exact_sha256(cosign_sha256)
    safe_port(registry_port)
    if not cosign_bin or Path(cosign_bin).name != "cosign":
        raise ValueError("cosign binary path must name the cosign executable")
    return {
        "schema_version": "full-manager-mvp/local-registry-signing-plan/v1",
        "registry_image": registry_image,
        "cosign_binary": cosign_bin,
        "cosign_binary_sha256": exact_sha256(cosign_sha256),
        "registry": {
            "host": "127.0.0.1",
            "port": registry_port,
            "repository": "manager-demo",
            "max_containers": 1,
        },
        "resource_budget": {
            "max_registry_containers": 1,
            "max_local_images_built": 1,
            "max_pushes": 1,
            "max_signatures": 1,
            "max_runtime_seconds": 600,
            "ephemeral_keypair_only": True,
            "external_registry_credentials": False,
        },
        "operations": [
            "verify the exact cosign binary SHA-256 before any signing operation",
            "refuse a busy loopback registry port and refuse takeover of the generated container name",
            "start one local registry container from an exact digest reference",
            "build the demo application locally from the pinned Dockerfile and push one image to the loopback registry",
            "parse the registry-returned pushed image digest and sign only the digest reference",
            "generate one ephemeral local cosign keypair with an in-memory password",
            "sign with transparency-log upload disabled and HTTP registry explicitly allowed for local testing",
            "verify the stored registry signature with the ephemeral public key and tlog verification explicitly disabled",
            "persist only non-secret digest/version/verification metadata",
            "remove the built local image tag, registry container, temporary key material and local staging files in finally",
        ],
        "forbidden_promotions": [
            "plan-only PASS to registry signing PASS",
            "local registry signature PASS to production registry signing",
            "ephemeral local keypair to production signing-key custody",
            "loopback registry to external registry credential readiness",
            "local signature verification to organization-wide supply-chain compliance",
            "local execution to production operations or people-management tenure",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded loopback registry + cosign image-signature proof.")
    parser.add_argument("--registry-image", required=True)
    parser.add_argument("--cosign-bin", required=True)
    parser.add_argument("--cosign-sha256", required=True)
    parser.add_argument("--registry-port", type=int, default=5001)
    parser.add_argument("--output", default="evidence/local-registry-signing/receipt.json")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    execution_plan = plan(
        registry_image=args.registry_image,
        cosign_bin=args.cosign_bin,
        cosign_sha256=args.cosign_sha256,
        registry_port=args.registry_port,
    )
    if args.plan_only:
        print(json.dumps(execution_plan, indent=2, sort_keys=True))
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    output = (repo_root / args.output).resolve()
    if repo_root not in output.parents:
        raise RuntimeError("--output must remain inside repository")

    cosign_path = Path(args.cosign_bin).expanduser().resolve()
    if not cosign_path.is_file():
        raise RuntimeError("cosign binary does not exist")
    if sha256_file(cosign_path) != exact_sha256(args.cosign_sha256):
        raise RuntimeError("cosign binary SHA-256 mismatch")

    for tool in ("git", "docker"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"required local tool missing: {tool}")
    run(["docker", "info"], cwd=repo_root, timeout=30)
    assert_port_free(args.registry_port)

    started = time.monotonic()
    subject = git_subject(repo_root)
    temp_root: Path | None = None
    registry_name = f"manager-demo-m6-registry-{subject['commit'][:8]}"
    registry_started = False
    built_local_tag: str | None = None
    cleanup_errors: list[str] = []
    receipt = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": subject,
        "plan": execution_plan,
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "cosign_binary_sha256_verified": "PASS",
            "registry_started_from_exact_digest": "NOT_EXERCISED",
            "image_pushed_by_digest": "NOT_EXERCISED",
            "ephemeral_keypair_generated": "NOT_EXERCISED",
            "registry_signature_uploaded": "NOT_EXERCISED",
            "registry_signature_verified": "NOT_EXERCISED",
            "local_image_removed": "NOT_EXERCISED",
            "cleanup": "NOT_EXERCISED",
            "production_registry_signing": "NOT_EXERCISED",
            "production_key_custody": "NOT_EXERCISED",
        },
    }

    try:
        existing = run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            cwd=repo_root,
            timeout=20,
        ).stdout.splitlines()
        if registry_name in existing:
            raise RuntimeError(f"refusing to take over existing container {registry_name}")
        temp_root = Path(tempfile.mkdtemp(prefix="manager-demo-m6-registry-"))
        key_prefix = temp_root / "ephemeral-cosign"

        run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "--name",
                registry_name,
                "-p",
                f"127.0.0.1:{args.registry_port}:5000",
                args.registry_image,
            ],
            cwd=repo_root,
            timeout=60,
        )
        registry_started = True
        receipt["checks"]["registry_started_from_exact_digest"] = "PASS"

        local_tag = f"127.0.0.1:{args.registry_port}/manager-demo:{subject['commit'][:12]}"
        built_local_tag = local_tag
        run(
            [
                "docker",
                "build",
                "-t",
                local_tag,
                "-f",
                "platform/docker/Dockerfile",
                "platform/app",
            ],
            cwd=repo_root,
            timeout=300,
        )
        pushed = run(["docker", "push", local_tag], cwd=repo_root, timeout=180).stdout
        matches = re.findall(r"digest:\s+(sha256:[0-9a-f]{64})", pushed)
        if not matches:
            raise RuntimeError("docker push output did not expose an exact registry digest")
        pushed_digest = matches[-1]
        digest_ref = f"127.0.0.1:{args.registry_port}/manager-demo@{pushed_digest}"
        receipt["checks"]["image_pushed_by_digest"] = "PASS"

        cosign_env = os.environ.copy()
        cosign_env["COSIGN_PASSWORD"] = secrets.token_urlsafe(24)
        run(
            [
                str(cosign_path),
                "generate-key-pair",
                "--output-key-prefix",
                str(key_prefix),
            ],
            cwd=repo_root,
            timeout=60,
            env=cosign_env,
        )
        key_file = Path(f"{key_prefix}.key")
        pub_file = Path(f"{key_prefix}.pub")
        if not key_file.is_file() or not pub_file.is_file():
            raise RuntimeError("cosign ephemeral keypair missing")
        receipt["checks"]["ephemeral_keypair_generated"] = "PASS"

        sign = run(
            [
                str(cosign_path),
                "sign",
                "--yes",
                "--key",
                str(key_file),
                "--allow-http-registry",
                "--tlog-upload=false",
                digest_ref,
            ],
            cwd=repo_root,
            timeout=120,
            env=cosign_env,
        )
        receipt["sign_output_tail"] = sign.stdout[-2000:]
        receipt["checks"]["registry_signature_uploaded"] = "PASS"

        verify = run(
            [
                str(cosign_path),
                "verify",
                "--key",
                str(pub_file),
                "--allow-http-registry",
                "--insecure-ignore-tlog",
                digest_ref,
            ],
            cwd=repo_root,
            timeout=120,
            env=cosign_env,
        )
        receipt["verify_output_tail"] = verify.stdout[-4000:]
        receipt["checks"]["registry_signature_verified"] = "PASS"
        receipt["result"] = {
            "image_digest_ref": digest_ref,
            "registry_image": args.registry_image,
            "cosign_binary_sha256": sha256_file(cosign_path),
            "cosign_version": run(
                [str(cosign_path), "version"],
                cwd=repo_root,
                timeout=20,
            ).stdout[:2000],
            "ephemeral_public_key_sha256": sha256_file(pub_file),
        }
        receipt["state"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"
    finally:
        if built_local_tag is not None:
            result = run(
                ["docker", "image", "rm", "-f", built_local_tag],
                cwd=repo_root,
                timeout=60,
                check=False,
            )
            if result.returncode == 0:
                receipt["checks"]["local_image_removed"] = "PASS"
            else:
                cleanup_errors.append("failed to remove built local image tag")
                receipt["checks"]["local_image_removed"] = "FAIL"
        if registry_started:
            result = run(
                ["docker", "rm", "-f", registry_name],
                cwd=repo_root,
                timeout=60,
                check=False,
            )
            if result.returncode != 0:
                cleanup_errors.append("failed to remove local registry container")
        if temp_root is not None:
            try:
                shutil.rmtree(temp_root)
            except Exception as exc:  # noqa: BLE001
                cleanup_errors.append(str(exc))
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
