from fastapi.testclient import TestClient

from manager_demo.main import create_app


def payload(key: str, *, model: str = "model-v1") -> dict[str, str]:
    return {
        "idempotency_key": key,
        "git_commit": "b" * 40,
        "model_version": model,
        "prompt_version": "prompt-v1",
        "config_version": "config-v1",
    }


def test_candidate_registration_is_idempotent() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    client = TestClient(app)
    first = client.post("/v1/candidates", json=payload("idem-key-0001"))
    second = client.post("/v1/candidates", json=payload("idem-key-0001"))
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["state"] == "REGISTERED"


def test_idempotency_key_conflict_fails_closed() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    client = TestClient(app)
    assert client.post("/v1/candidates", json=payload("idem-key-0002")).status_code == 200
    conflict = client.post("/v1/candidates", json=payload("idem-key-0002", model="different-model"))
    assert conflict.status_code == 409


def test_ready_requires_database() -> None:
    app = create_app(database_url="sqlite+pysqlite:///:memory:", create_schema=True)
    client = TestClient(app)
    assert client.get("/health/ready").json() == {"status": "ready"}
