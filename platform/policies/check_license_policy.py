from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FORBIDDEN = re.compile(r"(^|[^L])AGPL|(^|[^L])GPL|SSPL|COMMONS CLAUSE", re.IGNORECASE)
REVIEW = re.compile(r"LGPL|MPL|EPL|CDDL", re.IGNORECASE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    packages = json.loads(args.inventory.read_text(encoding="utf-8"))
    forbidden: list[dict[str, str]] = []
    review: list[dict[str, str]] = []
    for package in packages:
        name = str(package.get("Name", package.get("name", "UNKNOWN")))
        license_name = str(package.get("License", package.get("license", "UNKNOWN")))
        item = {"name": name, "license": license_name}
        if FORBIDDEN.search(license_name):
            forbidden.append(item)
        elif REVIEW.search(license_name):
            review.append(item)
    receipt = {
        "schema_version": "full-manager-mvp/license-policy/v1",
        "packages_observed": len(packages),
        "forbidden": forbidden,
        "review_required": review,
        "verdict": "PASS" if not forbidden else "FAIL",
        "evidence_ceiling": "INSTALLED_PYTHON_ENVIRONMENT_LICENSE_METADATA_ONLY_NOT_LEGAL_CLEARANCE",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if forbidden:
        raise SystemExit("forbidden dependency license detected")


if __name__ == "__main__":
    main()
