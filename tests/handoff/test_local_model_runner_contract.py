from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_local_model.py"
DUMMY_COMMIT = "1" * 40
DUMMY_SHA = "2" * 64
DUMMY_URL = "https://example.invalid/model.gguf"


class LocalModelRunnerContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--llama-commit", DUMMY_COMMIT,
                "--model-url", DUMMY_URL,
                "--model-sha256", DUMMY_SHA,
                "--model-license-id", "Apache-2.0",
                *extra,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )

    def test_plan_is_bounded_and_non_promoting(self) -> None:
        completed = self.run_plan()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        plan = json.loads(completed.stdout)
        self.assertEqual(plan["schema_version"], "full-manager-mvp/local-model-plan/v1")
        self.assertEqual(plan["llama_commit"], DUMMY_COMMIT)
        self.assertEqual(plan["model_sha256"], DUMMY_SHA)
        self.assertEqual(plan["model_license_id"], "Apache-2.0")
        self.assertLessEqual(plan["resource_budget"]["threads"], 8)
        self.assertLessEqual(plan["resource_budget"]["max_tokens"], 128)
        self.assertLessEqual(plan["resource_budget"]["timeout_seconds"], 300)
        self.assertFalse(plan["resource_budget"]["persistent_model_cache"])
        self.assertEqual(
            plan["evidence_ceiling_after_real_execution"],
            "LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY",
        )
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("production model traffic", joined)
        self.assertIn("real user adoption", joined)

    def test_short_llama_commit_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--llama-commit", "abc",
                "--model-url", DUMMY_URL,
                "--model-sha256", DUMMY_SHA,
                "--model-license-id", "Apache-2.0",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exact 40-hex", completed.stdout)

    def test_mutable_or_non_https_model_url_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--llama-commit", DUMMY_COMMIT,
                "--model-url", "http://example.invalid/model.gguf",
                "--model-sha256", DUMMY_SHA,
                "--model-license-id", "Apache-2.0",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("https://", completed.stdout)

    def test_wrong_license_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--llama-commit", DUMMY_COMMIT,
                "--model-url", DUMMY_URL,
                "--model-sha256", DUMMY_SHA,
                "--model-license-id", "UNKNOWN",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Apache-2.0", completed.stdout)

    def test_unbounded_threads_are_rejected(self) -> None:
        completed = self.run_plan("--threads", "64")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("threads must be between", completed.stdout)


if __name__ == "__main__":
    unittest.main()
