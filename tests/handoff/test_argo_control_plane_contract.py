from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_argo_control_plane.py"
DUMMY_CONTEXT = "kind-manager-demo-m6"
DUMMY_REVISION = "1" * 40
DUMMY_SHA_A = "2" * 64
DUMMY_SHA_B = "3" * 64
DUMMY_URL_A = "https://example.invalid/argocd.yaml"
DUMMY_URL_B = "https://example.invalid/rollouts.yaml"


class ArgoControlPlaneContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--cluster-context", DUMMY_CONTEXT,
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

    def test_plan_is_bounded_and_non_promoting(self) -> None:
        completed = self.run_plan()
        self.assertEqual(completed.returncode, 0, completed.stdout)
        plan = json.loads(completed.stdout)
        self.assertEqual(plan["schema_version"], "full-manager-mvp/local-argo-control-plane-plan/v1")
        self.assertEqual(plan["resource_budget"]["max_target_clusters"], 1)
        self.assertEqual(plan["resource_budget"]["max_manifest_downloads"], 2)
        self.assertEqual(plan["evidence_ceiling_after_real_execution"], "LOCAL_ARGO_CONTROLLERS_READY_ONLY")
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("application reconciliation", joined)
        self.assertIn("production deployment experience", joined)

    def test_non_manager_demo_context_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--cluster-context", "production",
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
        self.assertIn("kind-manager-demo", completed.stdout)

    def test_mutable_manifest_digest_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--cluster-context", DUMMY_CONTEXT,
                "--target-revision", DUMMY_REVISION,
                "--argocd-manifest-url", DUMMY_URL_A,
                "--argocd-manifest-sha256", "latest",
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
        self.assertIn("64 hex", completed.stdout)

    def test_non_https_manifest_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--cluster-context", DUMMY_CONTEXT,
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
