#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import compile_m7_advanced_queue as m7


def exact_sha40(name: str, value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise SystemExit(f"{name} must be an exact 40-hex Git SHA")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compile the advanced Local Handoff queue while binding predecessor "
            "receipts to an explicitly admitted execution subject."
        )
    )
    parser.add_argument("--expected-predecessor-commit", required=True)
    parser.add_argument("--expected-predecessor-tree", required=True)
    parser.add_argument(
        "--reviewer-receipt",
        default="evidence/local-reviewer/handoff-receipt.json",
    )
    parser.add_argument(
        "--kind-receipt",
        default="evidence/local-kind/local-kind-receipt.json",
    )
    parser.add_argument(
        "--output",
        default="handoff/m7-advanced-local-handoff-queue.json",
    )
    parser.add_argument(
        "--compile-receipt",
        default="evidence/receipts/handoff/m7-advanced-queue-compile-receipt.json",
    )
    parser.add_argument("--fixture-mode", action="store_true")
    args = parser.parse_args()

    # The underlying M7 compiler already owns schema, receipt admission,
    # queue construction, evidence ceilings and fixture/live separation.
    # This wrapper changes only the explicitly admitted predecessor subject.
    m7.PREDECESSOR_COMMIT = exact_sha40(
        "--expected-predecessor-commit", args.expected_predecessor_commit
    )
    m7.PREDECESSOR_TREE = exact_sha40(
        "--expected-predecessor-tree", args.expected_predecessor_tree
    )

    delegated = [
        str(Path(m7.__file__).resolve()),
        "--reviewer-receipt",
        args.reviewer_receipt,
        "--kind-receipt",
        args.kind_receipt,
        "--output",
        args.output,
        "--compile-receipt",
        args.compile_receipt,
    ]
    if args.fixture_mode:
        delegated.append("--fixture-mode")

    original_argv = sys.argv
    try:
        sys.argv = delegated
        return m7.main()
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    raise SystemExit(main())
