from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_live_kind_smoke.py"
DUMMY_NODE = "kindest/node:v-test@sha256:" + ("1" * 64)


class LiveKindRunnerContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--kind-node-image",
                DUMMY_NODE,
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
        self.assertEqual(plan["schema_version"], "full-manager-mvp/local-kind-plan/v1")
        self.assertEqual(plan["resource_budget"]["max_clusters_created"], 1)
        self.assertEqual(plan["resource_budget"]["deployment_replicas"], 2)
        self.assertLessEqual(plan["resource_budget"]["max_runtime_seconds"], 600)
        self.assertEqual(
            plan["evidence_ceiling_after_real_execution"],
            "LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY",
        )
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("production Kubernetes experience", joined)
        self.assertIn("1000-VU", joined)
        self.assertIn("production incident history", joined)

    def test_arbitrary_cluster_name_is_rejected(self) -> None:
        completed = self.run_plan("--cluster-name", "production")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("cluster name must match", completed.stdout)

    def test_mutable_kind_node_image_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--kind-node-image",
                "kindest/node:latest",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exact name@sha256", completed.stdout)

    def test_privileged_local_port_is_rejected(self) -> None:
        completed = self.run_plan("--local-port", "80")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("between 1024 and 65535", completed.stdout)


if __name__ == "__main__":
    unittest.main()
