from __future__ import annotations

import unittest

from run_failure_drills import (
    exercise_duplicate_side_effect,
    exercise_permission_failure,
    exercise_queue_pressure,
    exercise_restore_assumption,
)


class FailurePrimitiveTests(unittest.TestCase):
    def test_queue_pressure_retest(self) -> None:
        result = exercise_queue_pressure()
        self.assertEqual(result["verdict"], "PASS")
        self.assertTrue(result["observations"]["same_failure_retest"])

    def test_duplicate_side_effect_is_bounded(self) -> None:
        result = exercise_duplicate_side_effect()
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["observations"]["durable_effect_count"], 1)
        self.assertEqual(result["observations"]["conflict"], "CONFLICT")

    def test_permission_failure_fails_closed(self) -> None:
        result = exercise_permission_failure()
        self.assertEqual(result["verdict"], "PASS")
        self.assertTrue(result["observations"]["missing_scope_denied"])

    def test_restore_is_verified_and_repeatable(self) -> None:
        result = exercise_restore_assumption()
        self.assertEqual(result["verdict"], "PASS")
        self.assertTrue(result["observations"]["restore_verified"])
        self.assertTrue(result["observations"]["same_failure_retest"])


if __name__ == "__main__":
    unittest.main()
