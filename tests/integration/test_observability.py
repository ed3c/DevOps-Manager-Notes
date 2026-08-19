from fastapi.testclient import TestClient

from manager_demo.main import create_app


def test_trace_identity_and_metrics_are_exposed() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    with TestClient(app) as client:
        response = client.get("/health/live")
        assert response.status_code == 200
        trace_id = response.headers["X-Trace-Id"]
        assert len(trace_id) == 32
        assert int(trace_id, 16) != 0

        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "manager_demo_http_requests_total" in metrics.text
        assert "manager_demo_http_request_duration_seconds" in metrics.text


def test_business_failure_is_visible_while_transport_is_healthy() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    with TestClient(app) as client:
        payload = {
            "subject": {"git_commit": "a" * 40},
            "expected_value": "approved",
            "observed_value": "rejected",
        }
        response = client.post("/v1/oracle/evaluate", json=payload)
        assert response.status_code == 200
        assert response.json()["business_ok"] is False
        assert response.json()["evidence"]["verdict"] == "FAIL"
        assert client.get("/health/live").json()["status"] == "alive"
        metrics = client.get("/metrics").text
        assert 'manager_demo_business_oracle_total{verdict="FAIL"}' in metrics
