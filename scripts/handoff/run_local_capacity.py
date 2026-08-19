#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from urllib import request

SCHEMA = "full-manager-mvp/local-capacity-receipt/v1"
EVIDENCE_CEILING = "LOCAL_SYNTHETIC_1000_VU_ONLY"


def bounded_int(name: str, value: int, minimum: int, maximum: int) -> int:
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def bounded_float(name: str, value: float, minimum: float, maximum: float) -> float:
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def safe_port(value: int) -> int:
    return bounded_int("local_port", value, 1024, 65535)


def assert_port_free(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except OSError as exc:
            raise RuntimeError(f"local port {port} is already in use; refusing takeover") from exc


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


def wait_live(url: str, timeout_seconds: float = 15.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with request.urlopen(url, timeout=2) as response:
                body = json.load(response)
            if body.get("status") == "alive":
                return
        except Exception as exc:  # noqa: BLE001
            last = exc
        time.sleep(0.25)
    raise RuntimeError(f"local service did not become live: {last}")


def plan(*, users: int, spawn_rate: int, duration_seconds: int, p95_limit_ms: float, failure_ratio_limit: float, local_port: int) -> dict:
    bounded_int("users", users, 1, 1000)
    bounded_int("spawn_rate", spawn_rate, 1, 100)
    bounded_int("duration_seconds", duration_seconds, 5, 60)
    bounded_float("p95_limit_ms", p95_limit_ms, 1, 5000)
    bounded_float("failure_ratio_limit", failure_ratio_limit, 0.0, 0.10)
    safe_port(local_port)
    return {
        "schema_version": "full-manager-mvp/local-capacity-plan/v1",
        "workload": {
            "users": users,
            "spawn_rate": spawn_rate,
            "duration_seconds": duration_seconds,
            "host": f"http://127.0.0.1:{local_port}",
            "locustfile": "tests/load/locustfile.py",
        },
        "acceptance": {
            "p95_limit_ms": p95_limit_ms,
            "failure_ratio_limit": failure_ratio_limit,
        },
        "resource_budget": {
            "max_users": 1000,
            "max_spawn_rate_per_second": 100,
            "max_duration_seconds": 60,
            "loopback_only": True,
            "persistent_service": False,
            "pip_cache": False,
        },
        "operations": [
            "refuse to take over an occupied loopback port",
            "create a temporary Python virtual environment and install exact local app dev dependencies without a persistent pip cache",
            "start one loopback-only demo service on the requested high port",
            "run bounded Locust headless load against loopback only",
            "persist CSV statistics and evaluate aggregate failure ratio plus p95 latency",
            "terminate the service and remove the temporary virtual environment in finally",
        ],
        "forbidden_promotions": [
            "plan-only PASS to 1000-VU execution PASS",
            "1000 virtual users to 1000 real users",
            "local synthetic load to production capacity or adoption",
            "local latency to production SLO attainment",
            "synthetic capacity evidence to people-management tenure",
        ],
        "evidence_ceiling_after_real_execution": EVIDENCE_CEILING,
    }


def write_receipt(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def find_aggregate(stats_path: Path) -> dict[str, str]:
    if not stats_path.is_file():
        raise RuntimeError("Locust stats CSV missing")
    with stats_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row.get("Name") == "Aggregated":
            return row
    raise RuntimeError("Locust aggregate statistics row missing")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded loopback-only synthetic capacity runner.")
    parser.add_argument("--users", type=int, default=1000)
    parser.add_argument("--spawn-rate", type=int, default=100)
    parser.add_argument("--duration-seconds", type=int, default=30)
    parser.add_argument("--p95-limit-ms", type=float, default=1000.0)
    parser.add_argument("--failure-ratio-limit", type=float, default=0.01)
    parser.add_argument("--local-port", type=int, default=18040)
    parser.add_argument("--output", default="evidence/local-capacity/local-capacity-receipt.json")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    execution_plan = plan(
        users=args.users,
        spawn_rate=args.spawn_rate,
        duration_seconds=args.duration_seconds,
        p95_limit_ms=args.p95_limit_ms,
        failure_ratio_limit=args.failure_ratio_limit,
        local_port=args.local_port,
    )
    if args.plan_only:
        print(json.dumps(execution_plan, indent=2, sort_keys=True))
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    output = (repo_root / args.output).resolve()
    if repo_root not in output.parents:
        raise RuntimeError("--output must remain inside repository")

    started = time.monotonic()
    temp_root: Path | None = None
    service: subprocess.Popen[str] | None = None
    service_log = None
    cleanup_errors: list[str] = []
    receipt = {
        "schema_version": SCHEMA,
        "state": "FAIL",
        "subject": git_subject(repo_root),
        "plan": execution_plan,
        "evidence_ceiling": EVIDENCE_CEILING,
        "checks": {
            "loopback_port_free": "NOT_EXERCISED",
            "loopback_service_live": "NOT_EXERCISED",
            "locust_exit_zero": "NOT_EXERCISED",
            "aggregate_stats_present": "NOT_EXERCISED",
            "failure_ratio_within_limit": "NOT_EXERCISED",
            "p95_within_limit": "NOT_EXERCISED",
            "cleanup": "NOT_EXERCISED",
            "real_users": "NOT_EXERCISED",
            "production_capacity": "NOT_EXERCISED",
        },
    }

    try:
        if shutil.which("python3") is None:
            raise RuntimeError("python3 is required")
        assert_port_free(args.local_port)
        receipt["checks"]["loopback_port_free"] = "PASS"
        temp_root = Path(tempfile.mkdtemp(prefix="manager-demo-m6-capacity-"))
        venv = temp_root / "venv"
        run(["python3", "-m", "venv", str(venv)], cwd=repo_root, timeout=60)
        python_bin = venv / "bin" / "python"
        locust_bin = venv / "bin" / "locust"
        run(
            [
                str(python_bin), "-m", "pip", "install",
                "--disable-pip-version-check", "--no-input", "--no-cache-dir",
                "-e", "platform/app[dev]",
            ],
            cwd=repo_root,
            timeout=240,
        )

        env = os.environ.copy()
        env["DATABASE_URL"] = f"sqlite+pysqlite:///{temp_root / 'capacity.db'}"
        env["SOURCE_COMMIT"] = receipt["subject"]["commit"]
        service_log = (temp_root / "service.log").open("w", encoding="utf-8")
        service = subprocess.Popen(
            [str(python_bin), "-m", "uvicorn", "manager_demo.main:app", "--host", "127.0.0.1", "--port", str(args.local_port)],
            cwd=repo_root,
            env=env,
            text=True,
            stdout=service_log,
            stderr=subprocess.STDOUT,
        )
        wait_live(f"http://127.0.0.1:{args.local_port}/health/live")
        receipt["checks"]["loopback_service_live"] = "PASS"

        evidence_dir = output.parent
        evidence_dir.mkdir(parents=True, exist_ok=True)
        prefix = evidence_dir / "locust"
        completed = run(
            [
                str(locust_bin),
                "-f", "tests/load/locustfile.py",
                "--headless",
                "-u", str(args.users),
                "-r", str(args.spawn_rate),
                "-t", f"{args.duration_seconds}s",
                "--host", f"http://127.0.0.1:{args.local_port}",
                "--csv", str(prefix),
                "--exit-code-on-error", "1",
                "--only-summary",
            ],
            cwd=repo_root,
            env=env,
            timeout=args.duration_seconds + 120,
            check=False,
        )
        receipt["locust_output_tail"] = completed.stdout[-4000:]
        if completed.returncode != 0:
            raise RuntimeError(f"Locust exited {completed.returncode}")
        receipt["checks"]["locust_exit_zero"] = "PASS"

        stats_path = Path(f"{prefix}_stats.csv")
        aggregate = find_aggregate(stats_path)
        receipt["checks"]["aggregate_stats_present"] = "PASS"
        request_count = int(float(aggregate.get("Request Count") or 0))
        failure_count = int(float(aggregate.get("Failure Count") or 0))
        p95 = float(aggregate.get("95%") or 0)
        if request_count <= 0:
            raise RuntimeError("Locust produced no requests")
        failure_ratio = failure_count / request_count
        if failure_ratio > args.failure_ratio_limit:
            raise RuntimeError(f"failure ratio {failure_ratio:.6f} exceeded {args.failure_ratio_limit}")
        receipt["checks"]["failure_ratio_within_limit"] = "PASS"
        if p95 > args.p95_limit_ms:
            raise RuntimeError(f"p95 {p95:.3f} ms exceeded {args.p95_limit_ms}")
        receipt["checks"]["p95_within_limit"] = "PASS"
        receipt["result"] = {
            "users": args.users,
            "spawn_rate": args.spawn_rate,
            "duration_seconds": args.duration_seconds,
            "request_count": request_count,
            "failure_count": failure_count,
            "failure_ratio": failure_ratio,
            "p95_ms": p95,
            "stats_file": str(stats_path.relative_to(repo_root)),
        }
        receipt["state"] = "PASS"
    except Exception as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["state"] = "FAIL"
    finally:
        if service is not None:
            service.terminate()
            try:
                service.wait(timeout=5)
            except subprocess.TimeoutExpired:
                service.kill()
                service.wait(timeout=5)
        if service_log is not None:
            service_log.close()
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
