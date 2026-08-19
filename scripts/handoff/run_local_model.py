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

SCHEMA = "full-manager-mvp/local-model-receipt/v1"
EVIDENCE_CEILING = "LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY"
LLAMA_REPO = "https://github.com/ggml-org/llama.cpp.git"
DEFAULT_MAX_MODEL_BYTES = 1_500_000_000
HARD_MAX_MODEL_BYTES = 2_000_000_000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_sha40(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("llama.cpp commit must be an exact 40-hex Git SHA")
    return value


def exact_sha256(value: str) -> str:
    value = value.lower().removeprefix("sha256:")
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("model SHA-256 must contain exactly 64 hex characters")
    return value


def https_url(value: str) -> str:
    if not re.fullmatch(r"https://[^\s]+", value):
        raise ValueError("model URL must be an https:// URL")
    return value


def validate_license(value: str) -> str:
    if value != "Apache-2.0":
        raise ValueError("M6 selected Qwen demo artifact must declare Apache-2.0 before runtime admission")
    return value


def bounded_int(name: str, value: int, minimum: int, maximum: int) -> int:
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def run(argv: list[str], *, cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=True,
    )


def git_subject(repo_root: Path) -> dict[str, str]:
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, timeout=10).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", tree):
        raise RuntimeError("unable to bind exact repository subject")
    return {"repository": "ed3c/DevOps-Manager-Notes", "commit": commit, "tree": tree}


def download_limited(url: str, destination: Path, max_bytes: int) -> int:
    total = 0
    with request.urlopen(url, timeout=30) as response, destination.open("wb") as handle:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > max_bytes:
            raise RuntimeError(f"model Content-Length {content_length} exceeds max {max_bytes}")
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"model download exceeded max {max_bytes} bytes")
            handle.write(chunk)
    return total


def plan(*, llama_commit: str, model_url: str, model_sha256: str, model_license_id: str, threads: int, max_tokens: int, timeout_seconds: int, max_model_bytes: int) -> dict:
    exact_sha40(llama_commit)
    https_url(model_url)
    exact_sha256(model_sha256)
    validate_license(model_license_id)
    bounded_int("threads", threads, 1, 8)
    bounded_int("max_tokens", max_tokens, 1, 128)
    bounded_int("timeout_seconds", timeout_seconds, 30, 300)
    bounded_int("max_model_bytes", max_model_bytes, 1, HARD_MAX_MODEL_BYTES)
    return {
        "schema_version": "full-manager-mvp/local-model-plan/v1",
        "llama_repo": LLAMA_REPO,
        "llama_commit": llama_commit,
        "model_url": model_url,
        "model_sha256": exact_sha256(model_sha256),
        "model_license_id": model_license_id,
        "resource_budget": {
            "threads": threads,
            "max_tokens": max_tokens,
            "timeout_seconds": timeout_seconds,
            "max_model_bytes": max_model_bytes,
            "max_model_downloads": 1,
            "max_source_clones": 1,
            "build_parallelism": 2,
            "persistent_model_cache": False,
        },
        "operations": [
            "clone llama.cpp into temporary storage and detach at the exact commit",
            "build only llama-cli with parallelism capped at two",
            "download one HTTPS model artifact with a hard byte ceiling",
            "verify the model SHA-256 before execution",
            "run one bounded inference with fixed prompt/token/thread limits",
            "persist only receipt metadata and a bounded output digest/tail",
            "delete source/build/model temporary bytes in finally",
        ],
        "forbidden_promotions": [
            "plan-only PASS to local inference PASS",
            "local inference PASS to production model traffic",
            "local inference PASS to production latency or capacity",
            "model repository license text to transitive/runtime legal clearance",
            "local execution to real user adoption or people-management tenure",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded Local Handoff runner for llama.cpp + exact model artifact inference.")
    parser.add_argument("--llama-commit", required=True)
    parser.add_argument("--model-url", required=True)
    parser.add_argument("--model-sha256", required=True)
    parser.add_argument("--model-license-id", required=True)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--max-tokens", type=int, default=32)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--max-model-bytes", type=int, default=DEFAULT_MAX_MODEL_BYTES)
    parser.add_argument("--output", default="evidence/local-model/local-model-receipt.json")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    execution_plan = plan(
        llama_commit=args.llama_commit,
        model_url=args.model_url,
        model_sha256=args.model_sha256,
        model_license_id=args.model_license_id,
        threads=args.threads,
        max_tokens=args.max_tokens,
        timeout_seconds=args.timeout_seconds,
        max_model_bytes=args.max_model_bytes,
    )
    if args.plan_only:
        print(json.dumps(execution_plan, indent=2, sort_keys=True))
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    output = (repo_root / args.output).resolve()
    if repo_root not in output.parents:
        raise RuntimeError("--output must remain inside repository")

    started = time.monotonic()
    receipt = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": git_subject(repo_root),
        "plan": execution_plan,
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "llama_commit_checked_out": "NOT_EXERCISED",
            "model_download_within_budget": "NOT_EXERCISED",
            "model_sha256_verified": "NOT_EXERCISED",
            "llama_cli_built": "NOT_EXERCISED",
            "local_inference_exit_zero": "NOT_EXERCISED",
            "local_inference_output_nonempty": "NOT_EXERCISED",
            "cleanup": "NOT_EXERCISED",
            "production_model_traffic": "NOT_EXERCISED",
            "live_kubernetes": "NOT_EXERCISED",
            "load_1000_vu": "NOT_EXERCISED",
        },
    }
    temp_root: Path | None = None
    cleanup_errors: list[str] = []
    try:
        for tool in ("git", "cmake"):
            if shutil.which(tool) is None:
                raise RuntimeError(f"required local tool missing: {tool}")
        temp_root = Path(tempfile.mkdtemp(prefix="manager-demo-m6-model-"))
        source_dir = temp_root / "llama.cpp"
        model_path = temp_root / "model.gguf"

        run(["git", "clone", "--filter=blob:none", "--no-checkout", LLAMA_REPO, str(source_dir)], cwd=temp_root, timeout=90)
        run(["git", "fetch", "--depth=1", "origin", args.llama_commit], cwd=source_dir, timeout=90)
        run(["git", "checkout", "--detach", args.llama_commit], cwd=source_dir, timeout=30)
        observed_commit = run(["git", "rev-parse", "HEAD"], cwd=source_dir, timeout=10).stdout.strip()
        if observed_commit != args.llama_commit:
            raise RuntimeError("llama.cpp checkout did not match requested commit")
        receipt["checks"]["llama_commit_checked_out"] = "PASS"

        run(["cmake", "-S", ".", "-B", "build", "-DLLAMA_CURL=OFF", "-DGGML_NATIVE=OFF"], cwd=source_dir, timeout=120)
        run(["cmake", "--build", "build", "--target", "llama-cli", "--parallel", "2"], cwd=source_dir, timeout=180)
        llama_cli = source_dir / "build" / "bin" / "llama-cli"
        if not llama_cli.is_file():
            raise RuntimeError("llama-cli build artifact missing")
        receipt["checks"]["llama_cli_built"] = "PASS"

        downloaded_bytes = download_limited(args.model_url, model_path, args.max_model_bytes)
        receipt["checks"]["model_download_within_budget"] = "PASS"
        observed_model_sha = sha256_file(model_path)
        if observed_model_sha != exact_sha256(args.model_sha256):
            raise RuntimeError("model SHA-256 mismatch")
        receipt["checks"]["model_sha256_verified"] = "PASS"

        prompt = "Reply with one short word confirming local inference readiness."
        completed = run(
            [str(llama_cli), "-m", str(model_path), "-p", prompt, "-n", str(args.max_tokens), "-t", str(args.threads)],
            cwd=source_dir,
            timeout=args.timeout_seconds,
        )
        receipt["checks"]["local_inference_exit_zero"] = "PASS"
        output_text = completed.stdout.strip()
        if not output_text:
            raise RuntimeError("llama.cpp returned empty output")
        receipt["checks"]["local_inference_output_nonempty"] = "PASS"
        receipt["inference"] = {
            "output_sha256": hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
            "output_tail": output_text[-1000:],
            "model_sha256": observed_model_sha,
            "model_bytes": downloaded_bytes,
            "llama_commit": observed_commit,
            "model_license_id": args.model_license_id,
        }
        receipt["state"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"
    finally:
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

    print(json.dumps({"receipt": str(output.relative_to(repo_root)), "state": receipt["state"], "ceiling": EVIDENCE_CEILING}, sort_keys=True))
    return 0 if receipt["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
