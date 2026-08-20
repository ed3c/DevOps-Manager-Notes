from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "handoff"))

import admit_public_receipt_packet as policy  # noqa: E402
import compile_public_receipt_packet as core  # noqa: E402

FIXTURES = ROOT / "tests" / "handoff" / "fixtures" / "m9"
QUEUE = FIXTURES / "queue.json"


class PublicReceiptAdmissionPolicyTests(unittest.TestCase):
    def admit(
        self,
        assignments: dict[str, str],
        *,
        queue: Path = QUEUE,
        root: Path = FIXTURES,
    ) -> dict:
        return policy.admit_packet(
            repo_root=ROOT,
            queue_path=queue,
            receipt_roots=[root],
            receipt_assignments=assignments,
            max_receipt_bytes=core.DEFAULT_MAX_RECEIPT_BYTES,
            fixture_mode=True,
        )

    def temp_queue(
        self,
        *,
        states: list[str],
        active_item: str,
        receipt_mutations: dict[str, callable] | None = None,
    ) -> tuple[Path, Path]:
        temp = tempfile.TemporaryDirectory(dir=ROOT / "tests" / "handoff")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        queue = json.loads(QUEUE.read_text(encoding="utf-8"))
        queue["current"] = {"active_item": active_item, "state": "ACTIVE"}
        for item, state in zip(queue["items"], states, strict=True):
            item["state"] = state
        queue_path = root / "queue.json"
        queue_path.write_text(
            json.dumps(queue, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        for name in ("reviewer-pass.json", "kind-pass.json", "compile-pass.json"):
            value = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
            if receipt_mutations and name in receipt_mutations:
                receipt_mutations[name](value)
            (root / name).write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        return queue_path, root

    def test_current_active_reviewer_receipt_is_admitted(self) -> None:
        result = self.admit(
            {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"}
        )
        self.assertEqual(
            result["aggregate"]["state"], "HUMAN_QUEUE_ADVANCE_REQUIRED"
        )
        self.assertEqual(result["aggregate"]["next_item"], "M9-LIVE-KIND-002")
        self.assertFalse(result["aggregate"]["queue_mutated"])
        self.assertFalse(result["aggregate"]["queue_advanced"])
        self.assertFalse(
            result["admission_policy"]["future_blocked_receipts_accepted"]
        )

    def test_blocked_future_receipt_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "blocked future item"):
            self.admit(
                {
                    "M9-LOCAL-REVIEWER-001": "reviewer-pass.json",
                    "M9-LIVE-KIND-002": "kind-pass.json",
                }
            )

    def test_queue_progress_requires_complete_before_active(self) -> None:
        queue_path, root = self.temp_queue(
            states=["BLOCKED_BY_PREDECESSOR", "ACTIVE", "BLOCKED_BY_PREDECESSOR"],
            active_item="M9-LIVE-KIND-002",
        )
        with self.assertRaisesRegex(ValueError, "precedes ACTIVE item but is not COMPLETE"):
            self.admit(
                {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"},
                queue=queue_path,
                root=root,
            )

    def test_completed_item_cannot_carry_fail_receipt(self) -> None:
        def reviewer_fail(value: dict) -> None:
            value["state"] = "FAIL"

        queue_path, root = self.temp_queue(
            states=["COMPLETE", "ACTIVE", "BLOCKED_BY_PREDECESSOR"],
            active_item="M9-LIVE-KIND-002",
            receipt_mutations={"reviewer-pass.json": reviewer_fail},
        )
        with self.assertRaisesRegex(ValueError, "completed queue item.*FAIL"):
            self.admit(
                {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"},
                queue=queue_path,
                root=root,
            )

    def test_completed_prefix_plus_active_can_reach_completion_review(self) -> None:
        queue_path, root = self.temp_queue(
            states=["COMPLETE", "COMPLETE", "ACTIVE"],
            active_item="M9-COMPILE-QUEUE-003",
        )
        result = self.admit(
            {
                "M9-LOCAL-REVIEWER-001": "reviewer-pass.json",
                "M9-LIVE-KIND-002": "kind-pass.json",
                "M9-COMPILE-QUEUE-003": "compile-pass.json",
            },
            queue=queue_path,
            root=root,
        )
        self.assertEqual(
            result["aggregate"]["state"], "QUEUE_COMPLETION_REVIEW_REQUIRED"
        )
        self.assertEqual(result["aggregate"]["pass_count"], 3)

    def test_completed_prefix_without_active_receipt_requests_active_receipt(self) -> None:
        queue_path, root = self.temp_queue(
            states=["COMPLETE", "ACTIVE", "BLOCKED_BY_PREDECESSOR"],
            active_item="M9-LIVE-KIND-002",
        )
        result = self.admit(
            {"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"},
            queue=queue_path,
            root=root,
        )
        self.assertEqual(result["aggregate"]["state"], "ACTIVE_RECEIPT_REQUIRED")
        self.assertEqual(result["aggregate"]["next_item"], "M9-LIVE-KIND-002")

    def test_live_output_is_restricted_to_public_packet_directory(self) -> None:
        with self.assertRaisesRegex(ValueError, "evidence/local-handoff"):
            policy.resolve_output_path(ROOT, "README.md", fixture_mode=False)
        allowed = policy.resolve_output_path(
            ROOT,
            "evidence/local-handoff/public-receipt-packet.json",
            fixture_mode=False,
        )
        self.assertTrue(
            core.is_within(allowed, (ROOT / "evidence" / "local-handoff").resolve())
        )

    def test_protected_input_paths_include_queue_and_receipt(self) -> None:
        protected = policy.protected_input_paths(
            queue_path=QUEUE,
            roots=[FIXTURES.resolve()],
            assignments={"M9-LOCAL-REVIEWER-001": "reviewer-pass.json"},
        )
        self.assertIn(QUEUE.resolve(), protected)
        self.assertIn((FIXTURES / "reviewer-pass.json").resolve(), protected)

    def test_extended_access_token_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "sensitive key"):
            policy.assert_extended_sensitive_keys(
                {"access_token": "opaque-value-that-avoids-token-regex"},
                label="receipt",
            )

    def test_filesystem_root_receipt_root_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "filesystem root"):
            policy.validate_receipt_roots([Path(Path.cwd().anchor)])

    def test_receipt_root_count_is_bounded(self) -> None:
        temp_dirs = [tempfile.TemporaryDirectory() for _ in range(policy.MAX_RECEIPT_ROOTS + 1)]
        for temp in temp_dirs:
            self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(ValueError, "at most"):
            policy.validate_receipt_roots([Path(temp.name) for temp in temp_dirs])


if __name__ == "__main__":
    unittest.main()
