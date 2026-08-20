#!/usr/bin/env python3
"""Secret-free capability probe for the DevOps Manager local handoff lane.

This script does not install tools, mutate clusters, authenticate providers, or
read credential values. It only checks whether the fixed local prerequisites
for issue #2 are reachable and emits a sanitized JSON receipt.
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

SCHEMA = "devops-manager/local-capabilities/v1"
REQUIRED_TOOLS = {
    "git": ["git", "--version"],
    "docker": ["docker", "--version"],
    "kubectl": ["kubectl", "version", "--client=true", "--output=json"],
    "kind": ["kind", "version"],
}
OPTIONAL_TOOLS = {
    "git-town": ["git-town", "--version"],
}


def run_probe(argv: list[str], timeout: int = 10) -> dict[str, Any]:
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
            timeout=timeout,
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


def docker_daemon_probe(timeout: int = 10) -> dict[str, Any]:
    if shutil.which("docker") is None:
        return {"reachable": False, "exit_code": None, "server_version": None, "stderr": "docker not found"}
    try:
        completed = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "reachable": completed.returncode == 0,
            "exit_code": completed.returncode,
            "server_version": completed.stdout.strip()[:200],
            "stderr": completed.stderr.strip()[:1000],
        }
    except subprocess.TimeoutExpired:
        return {"reachable": False, "exit_code": None, "server_version": None, "stderr": "docker info timed out"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Path for the sanitized JSON receipt")
    args = parser.parse_args()

    required = {name: run_probe(argv) for name, argv in REQUIRED_TOOLS.items()}
    optional = {name: run_probe(argv) for name, argv in OPTIONAL_TOOLS.items()}
    daemon = docker_daemon_probe()

    missing = [name for name, result in required.items() if not result["present"] or result["exit_code"] != 0]
    if not daemon["reachable"]:
        missing.append("docker-daemon")

    verdict = "PASS" if not missing else "FAIL"
    receipt = {
        "schema_version": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject": {
            "repository": "ed3c/DevOps-Manager-Notes",
            "issue": 2,
        },
        "environment": {
            "platform_system": platform.system(),
            "platform_machine": platform.machine(),
            "python_version": platform.python_version(),
        },
        "required_tools": required,
        "optional_tools": optional,
        "docker_daemon": daemon,
        "missing_required_capabilities": missing,
        "verdict": verdict,
        "evidence_ceiling": "LOCAL_CAPABILITY_REACHABILITY_ONLY",
        "does_not_prove": [
            "application build correctness",
            "kind cluster creation",
            "Kubernetes deployment correctness",
            "production infrastructure experience",
            "Git Town correctness",
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "output": str(output), "missing": missing}))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
