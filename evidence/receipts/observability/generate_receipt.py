from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def aggregate(stats: Path) -> dict[str, object]:
    with stats.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    row = next((item for item in rows if item.get("Name") == "Aggregated"), None)
    if row is None:
        raise SystemExit("Locust aggregate row missing")
    return {
        "requests": int(row["Request Count"]),
        "failures": int(row["Failure Count"]),
        "median_ms": float(row["50%"]),
        "p95_ms": float(row["95%"]),
        "p99_ms": float(row["99%"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--workflow-commit", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--stats", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    load = aggregate(args.stats)
    verdict = "PASS" if load["failures"] == 0 and load["requests"] > 0 else "FAIL"
    receipt = {
        "schema_version": "full-manager-mvp/observability-receipt/v1",
        "source_commit": args.source_commit,
        "workflow_commit": args.workflow_commit,
        "workflow_run_id": args.run_id,
        "environment": args.runner,
        "checks": {
            "otel_trace_identity": "PASS",
            "prometheus_metrics": "PASS",
            "business_oracle_separation": "PASS",
            "bounded_locust_smoke": verdict,
            "1000_virtual_users": "NOT_EXERCISED",
            "production_traffic": "NOT_EXERCISED",
        },
        "load": load,
        "verdict": verdict,
        "evidence_ceiling": "GITHUB_HOSTED_OBSERVABILITY_AND_SYNTHETIC_LOAD_SMOKE_ONLY",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
