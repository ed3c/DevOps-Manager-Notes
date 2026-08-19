#!/usr/bin/env python3
"""Bounded, secret-free prerequisite probe for the Full Manager MVP local lane.

This probe checks local executable reachability only. It does not install tools,
modify clusters, authenticate providers, download models, read secret values, or
claim application/Kubernetes/ML runtime correctness.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "devops-manager/full-mvp-local-prerequisites/v1"
REQUIRED_TOOLS: dict[str, list[str]] = {
    "git": ["git", "--version"],
    "docker": ["docker", "--version"],
    "kubectl": ["kubectl", "version", "--client=true", "--output=json"],
    "kind": ["kind", "version"],
}
OPTIONAL_TOOLS: dict[str, list[str]] = {
    "git-town": ["git-town", "--version"],
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "argocd": ["argocd", "version", "--client"],
    "helm": ["helm", "version", "--short"],
    "cosign": ["cosign", "version"],
    "syft": ["syft", "version"],
    "trivy": ["trivy", "--version"],
}


def probe(argv: list[str], timeout_seconds: int = 10) -> dict[str, Any]:
    executable = shutil.which(argv[0])
    if executable is None:
        return {
            "present": False,
            "argv": argv,
            "exit_code": None,
            "stdout": "",
            "stderr": "executable not found",
        }
    try:
        completed = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "present": True,
            "argv": argv,
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip()[:2000],
            "stderr": completed.stderr.strip()[:2000],
        }
    except subprocess.TimeoutExpired:
        return {
            "present": True,
            "argv": argv,
            "exit_code": None,
            "stdout": "",
            "stderr": "probe timed out",
        }


def git_subject() -> dict[str, Any]:
    if shutil.which("git") is None:
        return {"commit": None, "tree": None, "clean": None}

    def git(*args: str) -> str | None:
        try:
            completed = subprocess.run(
                ["git", *args],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            return None
        return completed.stdout.strip() if completed.returncode == 0 else None

    status = git("status", "--porcelain")
    return {
        "commit": git("rev-parse", "HEAD"),
        "tree": git("rev-parse", "HEAD^{tree}"),
        "clean": status == "" if status is not None else None,
    }


def docker_daemon() -> dict[str, Any]:
    if shutil.which("docker") is None:
        return {
            "reachable": False,
            "exit_code": None,
            "server_version": None,
            "stderr": "docker not found",
        }
    try:
        completed = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return {
            "reachable": completed.returncode == 0,
            "exit_code": completed.returncode,
            "server_version": completed.stdout.strip()[:200],
            "stderr": completed.stderr.strip()[:1000],
        }
    except subprocess.TimeoutExpired:
        return {
            "reachable": False,
            "exit_code": None,
            "server_version": None,
            "stderr": "docker info timed out",
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    required = {name: probe(argv) for name, argv in REQUIRED_TOOLS.items()}
    optional = {name: probe(argv) for name, argv in OPTIONAL_TOOLS.items()}
    daemon = docker_daemon()
    subject = git_subject()

    missing_required = [
        name
        for name, result in required.items()
        if not result["present"] or result["exit_code"] != 0
    ]
    if not daemon["reachable"]:
        missing_required.append("docker-daemon")

    verdict = "PASS" if not missing_required else "FAIL"
    receipt = {
        "schema_version": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "ed3c/DevOps-Manager-Notes",
        "git_subject": subject,
        "environment": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        },
        "required_tools": required,
        "optional_tools": optional,
        "docker_daemon": daemon,
        "missing_required_capabilities": missing_required,
        "verdict": verdict,
        "evidence_ceiling": "LOCAL_PREREQUISITE_REACHABILITY_ONLY",
        "does_not_prove": [
            "application correctness",
            "database migration correctness",
            "container build correctness",
            "kind cluster creation",
            "Kubernetes deployment correctness",
            "Argo CD or Rollouts correctness",
            "MLflow or local-model execution",
            "fault-injection correctness",
            "production infrastructure experience",
            "real organizational adoption",
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "output": str(output), "missing": missing_required}))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
