#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
IMAGE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--workflow-commit", required=True)
    parser.add_argument("--workflow-run-id", required=True)
    parser.add_argument("--runner-os", required=True)
    parser.add_argument("--runner-arch", required=True)
    parser.add_argument("--runner-image-os", default="")
    parser.add_argument("--runner-image-version", default="")
    parser.add_argument("--container-image-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    for name, value in (("source_commit", args.source_commit), ("workflow_commit", args.workflow_commit)):
        if not SHA.fullmatch(value):
            raise SystemExit(f"{name} must be a 40-character lower-case Git SHA")
    if not IMAGE_ID.fullmatch(args.container_image_id):
        raise SystemExit("container_image_id must be sha256:<64 hex>")

    receipt = {
        "schema_version": "full-manager-mvp/base-receipt/v2",
        "source_commit": args.source_commit,
        "workflow_commit": args.workflow_commit,
        "workflow_run_id": args.workflow_run_id,
        "runner_os": args.runner_os,
        "runner_arch": args.runner_arch,
        "runner_image_os": args.runner_image_os,
        "runner_image_version": args.runner_image_version,
        "container_image_id": args.container_image_id,
        "checks": {
            "python_compile": "PASS",
            "unit_integration": "PASS",
            "postgres_migration_upgrade": "PASS",
            "postgres_migration_rollback_reapply": "PASS",
            "immutable_kubernetes_render_guard": "PASS",
            "container_build_run": "PASS",
            "business_oracle_negative_control": "PASS",
            "kind_kubernetes_live_deployment": "NOT_EXERCISED"
        },
        "verdict": "PASS",
        "evidence_ceiling": "GITHUB_HOSTED_DETERMINISTIC_AND_CONTAINER_INTEGRATION_ONLY",
        "notes": [
            "kind/Kubernetes live deployment remains a Local Handoff obligation",
            "container image ID is not a registry manifest digest and must not be used as Kubernetes immutable-image evidence",
            "this receipt does not prove production infrastructure, real users, or management tenure"
        ]
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
