from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "handoff"))

import compile_public_receipt_packet as packet  # noqa: E402

FIXTURES = ROOT / "tests" / "handoff" / "fixtures" / "m9"
QUEUE = FIXTURES / "queue.json"


class PublicReceiptPacketTests(unittest.TestCase):
    def compile(
        self,
        assignments: dict[str, str],
        *,
        fixture_mode: bool = True,
        max_bytes: int = packet.DEFAULT_MAX_RECEIPT_BYTES,
        root: Path = FIXTURES,
    ) -> dict:
        return packet.compile_packet(
            repo_root=ROOT,
            queue_path=QUEUE,
            receipt_roots=[root],
            receipt_assignments=assignments,
            max_receipt_bytes=max_bytes,
            fixture_mode=fixture_mode,
        )

    def mutate(self, name: str, mutate) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        value = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        mutate(value)
        path = root / name
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return temp, path

    def test_reviewer_pass_compiles_public_safe_prefix_packet(self) -> None:
        result = self.compile(
            {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"}
        )
        self.assertEqual(result["evidence_kind"], "FIXTURE")
        self.assertEqual(
            result["evidence_ceiling"],
            "FIXTURE_PUBLIC_RECEIPT_PACKET_ONLY",
        )
        self.assertEqual(
            result["aggregate"]["state"],
            "HUMAN_QUEUE_ADVANCE_REQUIRED",
        )
        self.assertEqual(
            result["aggregate"]["next_item"],
            "M9-LIVE-KIND-002",
        )
        serialized = json.dumps(result, sort_keys=True)
        self.assertNotIn("SHOULD_NOT_APPEAR_IN_PUBLIC_PACKET", serialized)
        self.assertFalse(result["aggregate"]["queue_mutated"])
        self.assertFalse(result["aggregate"]["queue_advanced"])

    def test_full_prefix_requires_queue_completion_review(self) -> None:
        result = self.compile(
            {
                "M9-LOCAL-REVIEWER-001": "reviewer-pass.json",
                "M9-LIVE-KIND-002": "kind-pass.json",
                "M9-COMPILE-QUEUE-003": "compile-pass.json",
            }
        )
        self.assertEqual(
            result["aggregate"]["state"],
            "QUEUE_COMPLETION_REVIEW_REQUIRED",
        )
        self.assertIsNone(result["aggregate"]["next_item"])
        self.assertEqual(result["aggregate"]["pass_count"], 3)
        self.assertEqual(result["aggregate"]["fail_count"], 0)

    def test_fail_receipt_is_valid_evidence_but_opens_local_gap(self) -> None:
        temp, path = self.mutate(
            "reviewer-pass.json",
            lambda value: value.__setitem__("state", "FAIL"),
        )
        result = self.compile(
            {"M9-LOCAL-REVIEWER-001": path.name},
            root=Path(temp.name),
        )
        self.assertEqual(result["aggregate"]["state"], "LOCAL_GAP_OPEN")
        self.assertEqual(
            result["aggregate"]["next_item"],
            "M9-LOCAL-REVIEWER-001",
        )
        self.assertEqual(result["receipts"][0]["verdict"], "FAIL")

    def test_noncontiguous_receipt_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "contiguous prefix"):
            self.compile({"M9-LIVE-KIND-002": "kind-pass.json"})

    def test_wrong_subject_is_rejected(self) -> None:
        temp, path = self.mutate(
            "reviewer-pass.json",
            lambda value: value["subject"].__setitem__("commit", "f" * 40),
        )
        with self.assertRaisesRegex(ValueError, "does not match queue subject"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                root=Path(temp.name),
            )

    def test_wrong_ceiling_is_rejected(self) -> None:
        temp, path = self.mutate(
            "reviewer-pass.json",
            lambda value: value.__setitem__("evidence_ceiling", "PRODUCTION"),
        )
        with self.assertRaisesRegex(ValueError, "evidence ceiling mismatch"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                root=Path(temp.name),
            )

    def test_fixture_is_rejected_in_live_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "fixture receipt is forbidden"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"},
                fixture_mode=False,
            )

    def test_nonfixture_is_rejected_in_fixture_mode(self) -> None:
        temp, path = self.mutate(
            "reviewer-pass.json",
            lambda value: value.pop("evidence_kind"),
        )
        with self.assertRaisesRegex(
            ValueError,
            "must declare evidence_kind=FIXTURE",
        ):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                root=Path(temp.name),
            )

    def test_missing_cleanup_is_rejected_even_for_fail_receipt(self) -> None:
        def mutate(value: dict) -> None:
            value["state"] = "FAIL"
            value["checks"]["generated_workspace_cleanup"] = "NOT_EXERCISED"

        temp, path = self.mutate("reviewer-pass.json", mutate)
        with self.assertRaisesRegex(ValueError, "generated_workspace_cleanup"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                root=Path(temp.name),
            )

    def test_secret_like_material_is_rejected(self) -> None:
        def mutate(value: dict) -> None:
            value["api_key"] = "sk-" + "A" * 32

        temp, path = self.mutate("reviewer-pass.json", mutate)
        with self.assertRaisesRegex(ValueError, "secret-like|sensitive key"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                root=Path(temp.name),
            )

    def test_oversized_receipt_is_rejected(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        value = json.loads(
            (FIXTURES / "reviewer-pass.json").read_text(encoding="utf-8")
        )
        value["padding"] = "x" * 5000
        path = root / "reviewer-pass.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exceeds byte budget"):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": path.name},
                max_bytes=1000,
                root=root,
            )

    def test_compile_receipt_cannot_claim_physical_runtime(self) -> None:
        temp, path = self.mutate(
            "compile-pass.json",
            lambda value: value.__setitem__("physical_runtime_executed", True),
        )
        root = Path(temp.name)
        for name in ("reviewer-pass.json", "kind-pass.json"):
            (root / name).write_text(
                (FIXTURES / name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        with self.assertRaisesRegex(
            ValueError,
            "physical_runtime_executed=false",
        ):
            self.compile(
                {
                    "M9-LOCAL-REVIEWER-001": "reviewer-pass.json",
                    "M9-LIVE-KIND-002": "kind-pass.json",
                    "M9-COMPILE-QUEUE-003": path.name,
                },
                root=root,
            )

    def test_path_outside_admitted_root_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "outside every admitted receipt root",
        ):
            self.compile(
                {"M9-LOCAL-REVIEWER-001": "../../etc/passwd"}
            )


if __name__ == "__main__":
    unittest.main()
