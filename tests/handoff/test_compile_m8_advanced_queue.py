from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "scripts" / "handoff" / "compile_m8_advanced_queue.py"
FIXTURES = ROOT / "tests" / "handoff" / "fixtures" / "m7"
PREDECESSOR_COMMIT = "4cc3e162c00a3af240bab9e62482e07bb3e4f9a1"
PREDECESSOR_TREE = "5ff3349c1eb5c7976263c2e89347a353ccbc1072"


class M8AdvancedQueueWrapperTests(unittest.TestCase):
    def run_wrapper(
        self,
        *,
        expected_commit: str = PREDECESSOR_COMMIT,
        expected_tree: str = PREDECESSOR_TREE,
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        output = Path(temp.name) / "queue.json"
        receipt = Path(temp.name) / "compile-receipt.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(WRAPPER),
                "--fixture-mode",
                "--expected-predecessor-commit",
                expected_commit,
                "--expected-predecessor-tree",
                expected_tree,
                "--reviewer-receipt",
                str(FIXTURES / "reviewer-pass.json"),
                "--kind-receipt",
                str(FIXTURES / "kind-pass.json"),
                "--output",
                str(output),
                "--compile-receipt",
                str(receipt),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        return completed, output

    def test_explicit_admitted_subject_compiles_fixture_queue(self) -> None:
        completed, output = self.run_wrapper()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        queue = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(
            queue["schema_version"],
            "agentic-tech-lead/local-handoff-queue/v1",
        )
        self.assertEqual(queue["current"]["active_item"], "M7-ARGO-CONTROLLERS-001")

    def test_wrong_admitted_subject_is_rejected(self) -> None:
        completed, _ = self.run_wrapper(expected_commit="f" * 40)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("predecessor commit mismatch", completed.stdout)

    def test_malformed_subject_is_rejected_before_delegation(self) -> None:
        completed, _ = self.run_wrapper(expected_commit="main")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exact 40-hex", completed.stdout)

    def test_help_exposes_both_exact_subject_inputs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(WRAPPER), "--help"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("--expected-predecessor-commit", completed.stdout)
        self.assertIn("--expected-predecessor-tree", completed.stdout)


if __name__ == "__main__":
    unittest.main()
