from fastapi.testclient import TestClient

from manager_demo.main import create_app

GIT_SHA = "a" * 40


def subject() -> dict[str, str]:
    return {"git_commit": GIT_SHA}


def test_business_oracle_can_fail_while_service_is_live() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    client = TestClient(app)
    assert client.get("/health/live").json() == {"status": "alive"}
    response = client.post("/v1/oracle/evaluate", json={"subject": subject(), "expected_value": "approved", "observed_value": "rejected"})
    assert response.status_code == 200
    body = response.json()
    assert body["infrastructure_http_ok"] is True
    assert body["business_ok"] is False
    assert body["evidence"]["verdict"] == "FAIL"
    assert body["evidence"]["reason_codes"] == ["BUSINESS_ORACLE_MISMATCH"]
    assert client.get("/health/live").status_code == 200


def test_business_oracle_pass_binds_subject_identity() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    client = TestClient(app)
    response = client.post("/v1/oracle/evaluate", json={"subject": subject(), "expected_value": "approved", "observed_value": "approved"})
    body = response.json()
    assert body["business_ok"] is True
    assert body["evidence"]["verdict"] == "PASS"
    assert body["evidence"]["subject"]["git_commit"] == GIT_SHA
