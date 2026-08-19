from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPILER = ROOT / "scripts" / "handoff" / "compile_m7_advanced_queue.py"
FIXTURES = ROOT / "tests" / "handoff" / "fixtures" / "m7"
REVIEWER = FIXTURES / "reviewer-pass.json"
KIND = FIXTURES / "kind-pass.json"


class M7AdvancedQueueCompilerTests(unittest.TestCase):
    def run_compiler(
        self,
        *,
        reviewer: Path = REVIEWER,
        kind: Path = KIND,
        fixture_mode: bool = True,
    ) -> tuple[subprocess.CompletedProcess[str], Path | None]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        out = Path(temp.name) / "queue.json"
        receipt = Path(temp.name) / "compile-receipt.json"
        argv = [
            sys.executable,
            str(COMPILER),
            "--reviewer-receipt", str(reviewer),
            "--kind-receipt", str(kind),
            "--output", str(out),
            "--compile-receipt", str(receipt),
        ]
        if fixture_mode:
            argv.append("--fixture-mode")
        completed = subprocess.run(
            argv,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        return completed, out if out.exists() else None

    def mutate(self, source: Path, mutate) -> Path:
        temp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        self.addCleanup(lambda: Path(temp.name).unlink(missing_ok=True))
        value = json.loads(source.read_text(encoding="utf-8"))
        mutate(value)
        json.dump(value, temp)
        temp.close()
        return Path(temp.name)

    def test_fixture_compiles_one_active_canonical_queue(self) -> None:
        completed, output = self.run_compiler()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        assert output is not None
        queue = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(queue["schema_version"], "agentic-tech-lead/local-handoff-queue/v1")
        self.assertEqual(queue["current"], {"active_item": "M7-ARGO-CONTROLLERS-001", "state": "ACTIVE"})
        states = [item["state"] for item in queue["items"]]
        self.assertEqual(states, ["ACTIVE", "BLOCKED_BY_PREDECESSOR", "BLOCKED_BY_PREDECESSOR", "BLOCKED_BY_PREDECESSOR"])
        subject = queue["subject"]["commit"]
        self.assertTrue(all(item["entry"]["required_subject_commit"] == subject for item in queue["items"]))
        self.assertEqual(queue["items"][0]["runtime_lane"]["class"], "LOCAL_HOST")
        self.assertIn("queue_advance", queue["authority"]["automation_forbidden"])
        self.assertIn("semantic_conflict_resolution", queue["authority"]["automation_forbidden"])
        self.assertEqual(queue["items"][2]["runtime_lane"]["commands"][0]["argv"][3], "--users")
        self.assertIn("1000", queue["items"][2]["runtime_lane"]["commands"][0]["argv"])

    def test_fixture_is_rejected_without_fixture_mode(self) -> None:
        completed, _ = self.run_compiler(fixture_mode=False)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("fixture receipt is forbidden", completed.stdout)

    def test_absent_predecessor_receipt_is_rejected(self) -> None:
        completed, _ = self.run_compiler(reviewer=FIXTURES / "missing.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("required predecessor receipt is absent", completed.stdout)

    def test_reviewer_fail_is_rejected(self) -> None:
        reviewer = self.mutate(REVIEWER, lambda value: value.__setitem__("state", "FAIL"))
        completed, _ = self.run_compiler(reviewer=reviewer)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("reviewer receipt must be PASS", completed.stdout)

    def test_kind_fail_is_rejected(self) -> None:
        kind = self.mutate(KIND, lambda value: value.__setitem__("verdict", "FAIL"))
        completed, _ = self.run_compiler(kind=kind)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("kind receipt must have verdict PASS", completed.stdout)

    def test_wrong_subject_is_rejected(self) -> None:
        reviewer = self.mutate(REVIEWER, lambda value: value["subject"].__setitem__("commit", "f" * 40))
        completed, _ = self.run_compiler(reviewer=reviewer)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("predecessor commit mismatch", completed.stdout)

    def test_wrong_ceiling_is_rejected(self) -> None:
        kind = self.mutate(KIND, lambda value: value.__setitem__("evidence_ceiling", "PRODUCTION"))
        completed, _ = self.run_compiler(kind=kind)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("kind evidence ceiling mismatch", completed.stdout)


if __name__ == "__main__":
    unittest.main()
