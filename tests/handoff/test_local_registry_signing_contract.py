from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "handoff" / "run_local_registry_signing.py"
DUMMY_REGISTRY = "registry.example.invalid/distribution@sha256:" + ("1" * 64)
DUMMY_COSIGN_SHA = "2" * 64


class LocalRegistrySigningContractTests(unittest.TestCase):
    def run_plan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--registry-image", DUMMY_REGISTRY,
                "--cosign-bin", "/usr/local/bin/cosign",
                "--cosign-sha256", DUMMY_COSIGN_SHA,
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
        self.assertEqual(plan["schema_version"], "full-manager-mvp/local-registry-signing-plan/v1")
        self.assertEqual(plan["registry"]["host"], "127.0.0.1")
        self.assertEqual(plan["resource_budget"]["max_registry_containers"], 1)
        self.assertEqual(plan["resource_budget"]["max_signatures"], 1)
        self.assertTrue(plan["resource_budget"]["ephemeral_keypair_only"])
        self.assertFalse(plan["resource_budget"]["external_registry_credentials"])
        self.assertEqual(
            plan["evidence_ceiling_after_real_execution"],
            "LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY",
        )
        joined = "\n".join(plan["forbidden_promotions"])
        self.assertIn("production registry signing", joined)
        self.assertIn("production signing-key custody", joined)

    def test_mutable_registry_image_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--registry-image", "registry:latest",
                "--cosign-bin", "/usr/local/bin/cosign",
                "--cosign-sha256", DUMMY_COSIGN_SHA,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("name@sha256", completed.stdout)

    def test_invalid_cosign_digest_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--registry-image", DUMMY_REGISTRY,
                "--cosign-bin", "/usr/local/bin/cosign",
                "--cosign-sha256", "latest",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("64 hex", completed.stdout)

    def test_non_cosign_binary_name_is_rejected(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--plan-only",
                "--registry-image", DUMMY_REGISTRY,
                "--cosign-bin", "/usr/local/bin/tool",
                "--cosign-sha256", DUMMY_COSIGN_SHA,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("cosign executable", completed.stdout)

    def test_privileged_registry_port_is_rejected(self) -> None:
        completed = self.run_plan("--registry-port", "443")
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("between 1024 and 65535", completed.stdout)


if __name__ == "__main__":
    unittest.main()
