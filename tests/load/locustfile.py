from __future__ import annotations

import os

from locust import HttpUser, between, task

SOURCE_COMMIT = os.getenv("SOURCE_COMMIT", "0" * 40)


class ManagerDemoUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task(4)
    def liveness(self) -> None:
        with self.client.get("/health/live", name="GET /health/live", catch_response=True) as response:
            if response.status_code != 200 or response.json().get("status") != "alive":
                response.failure("liveness oracle failed")

    @task(1)
    def business_happy_path(self) -> None:
        payload = {
            "subject": {"git_commit": SOURCE_COMMIT},
            "expected_value": "approved",
            "observed_value": "approved",
        }
        with self.client.post(
            "/v1/oracle/evaluate",
            json=payload,
            name="POST /v1/oracle/evaluate happy",
            catch_response=True,
        ) as response:
            body = response.json()
            if response.status_code != 200 or not body.get("business_ok"):
                response.failure("business oracle did not admit happy path")
