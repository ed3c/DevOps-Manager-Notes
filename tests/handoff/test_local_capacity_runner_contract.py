from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_local_capacity.py"


class LocalCapacityContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RUNNER), "--plan-only", *extra],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )

    def test_default_plan_targets_1000_vu_with_bounds(self) -> None:
        completed = self.run_plan()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        plan = json.loads(completed.stdout)
        self.assertEqual(plan["workload"]["users"], 1000)
        self.assertTrue(plan["resource_budget"]["loopback_only"])
        self.assertEqual(plan["resource_budget"]["max_users"], 1000)
        self.assertLessEqual(plan["resource_budget"]["max_duration_seconds"], 60)
        self.assertEqual(plan["evidence_ceiling_after_real_execution"], "LOCAL_SYNTHETIC_1000_VU_ONLY")
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("1000 virtual users to 1000 real users", joined)
        self.assertIn("production capacity", joined)

    def test_more_than_1000_users_is_rejected(self) -> None:
        completed = self.run_plan("--users", "1001")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("users must be between", completed.stdout)

    def test_excessive_spawn_rate_is_rejected(self) -> None:
        completed = self.run_plan("--spawn-rate", "101")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("spawn_rate must be between", completed.stdout)

    def test_excessive_duration_is_rejected(self) -> None:
        completed = self.run_plan("--duration-seconds", "120")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("duration_seconds must be between", completed.stdout)

    def test_privileged_port_is_rejected(self) -> None:
        completed = self.run_plan("--local-port", "80")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("local_port must be between", completed.stdout)


if __name__ == "__main__":
    unittest.main()
