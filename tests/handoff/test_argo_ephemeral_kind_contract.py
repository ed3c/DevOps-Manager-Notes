from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_argo_ephemeral_kind.py"
DUMMY_NODE = "kindest/node@sha256:" + "1" * 64
DUMMY_REVISION = "2" * 40
DUMMY_SHA_A = "3" * 64
DUMMY_SHA_B = "4" * 64
DUMMY_URL_A = "https://example.invalid/argocd.yaml"
DUMMY_URL_B = "https://example.invalid/rollouts.yaml"


class ArgoEphemeralKindContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--kind-node-image", DUMMY_NODE,
                "--target-revision", DUMMY_REVISION,
                "--argocd-manifest-url", DUMMY_URL_A,
                "--argocd-manifest-sha256", DUMMY_SHA_A,
                "--rollouts-manifest-url", DUMMY_URL_B,
                "--rollouts-manifest-sha256", DUMMY_SHA_B,
                *extra,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )

    def test_plan_owns_one_ephemeral_cluster_and_cleanup(self) -> None:
        completed = self.run_plan()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        plan = json.loads(completed.stdout)
        self.assertEqual(plan["cluster_name"], "manager-demo-m7-argo")
        self.assertEqual(plan["cluster_context"], "kind-manager-demo-m7-argo")
        self.assertEqual(plan["resource_budget"]["max_clusters_created"], 1)
        self.assertTrue(plan["resource_budget"]["cluster_cleanup_required"])
        self.assertTrue(plan["resource_budget"]["kubectl_context_restore_required"])
        self.assertEqual(plan["resource_budget"]["max_manifest_bytes_each"], 20_000_000)
        self.assertEqual(
            plan["evidence_ceiling_after_real_execution"],
            "LOCAL_ARGO_CONTROLLERS_READY_ONLY",
        )
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("Application reconciliation", joined)
        self.assertIn("production Kubernetes", joined)

    def test_mutable_kind_image_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--kind-node-image", "kindest/node:latest",
                "--target-revision", DUMMY_REVISION,
                "--argocd-manifest-url", DUMMY_URL_A,
                "--argocd-manifest-sha256", DUMMY_SHA_A,
                "--rollouts-manifest-url", DUMMY_URL_B,
                "--rollouts-manifest-sha256", DUMMY_SHA_B,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("name@sha256", completed.stdout)

    def test_unscoped_cluster_name_is_rejected(self) -> None:
        completed = self.run_plan("--cluster-name", "production")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("manager-demo", completed.stdout)

    def test_non_https_manifest_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--kind-node-image", DUMMY_NODE,
                "--target-revision", DUMMY_REVISION,
                "--argocd-manifest-url", "http://example.invalid/argocd.yaml",
                "--argocd-manifest-sha256", DUMMY_SHA_A,
                "--rollouts-manifest-url", DUMMY_URL_B,
                "--rollouts-manifest-sha256", DUMMY_SHA_B,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("https://", completed.stdout)


if __name__ == "__main__":
    unittest.main()
