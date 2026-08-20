from __future__ import annotations

import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .contracts import (
    BusinessOracleRequest,
    BusinessOracleResponse,
    CandidateCreate,
    CandidateView,
    EvidenceEnvelope,
    EvidenceLane,
    EvidenceState,
)
from .db import Base, Database
from .observability import install_observability, record_business_oracle
from .repository import IdempotencyConflict, register_candidate


def _database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "sqlite+pysqlite:///./manager-demo.db",
    )


def create_app(
    *,
    database_url: str | None = None,
    create_schema: bool = False,
) -> FastAPI:
    app = FastAPI(title="Full Manager MVP Control Plane", version="0.1.0")
    install_observability(app)
    db = Database(database_url or _database_url())
    app.state.db = db

    if create_schema:
        Base.metadata.create_all(db.engine)

    def session_dependency(request: Request):
        yield from request.app.state.db.sessions()

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready")
    def ready(session: Session = Depends(session_dependency)) -> dict[str, str]:
        try:
            session.execute(text("SELECT 1"))
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="database not ready",
            ) from exc
        return {"status": "ready"}

    @app.post("/v1/candidates", response_model=CandidateView)
    def create_candidate(
        payload: CandidateCreate,
        session: Session = Depends(session_dependency),
    ) -> CandidateView:
        try:
            return register_candidate(session, payload)
        except IdempotencyConflict as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc

    @app.post("/v1/oracle/evaluate", response_model=BusinessOracleResponse)
    def evaluate_business(payload: BusinessOracleRequest) -> BusinessOracleResponse:
        ok = payload.expected_value == payload.observed_value and not payload.force_failure
        record_business_oracle(ok)
        verdict = EvidenceState.PASS if ok else EvidenceState.FAIL
        reasons = [] if ok else ["BUSINESS_ORACLE_MISMATCH"]
        return BusinessOracleResponse(
            business_ok=ok,
            evidence=EvidenceEnvelope(
                subject=payload.subject,
                lane=EvidenceLane.L2,
                verdict=verdict,
                reason_codes=reasons,
            ),
        )

    @app.get("/v1/evidence/schema")
    def evidence_schema() -> dict[str, object]:
        return EvidenceEnvelope.model_json_schema()

    return app


app = create_app()
