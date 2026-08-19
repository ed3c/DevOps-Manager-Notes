from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from .contracts import CandidateCreate, CandidateState, CandidateView
from .models import CandidateRecord


class IdempotencyConflict(RuntimeError):
    pass


def _payload_hash(payload: CandidateCreate) -> str:
    body = payload.model_dump(exclude={"idempotency_key"})
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def register_candidate(session: Session, payload: CandidateCreate) -> CandidateView:
    existing = session.scalar(
        select(CandidateRecord).where(
            CandidateRecord.idempotency_key == payload.idempotency_key
        )
    )
    digest = _payload_hash(payload)

    if existing is not None:
        if existing.payload_hash != digest:
            raise IdempotencyConflict(
                "idempotency key already exists with a different payload"
            )
        return CandidateView(
            id=existing.id,
            idempotency_key=existing.idempotency_key,
            git_commit=existing.git_commit,
            model_version=existing.model_version,
            prompt_version=existing.prompt_version,
            config_version=existing.config_version,
            state=CandidateState(existing.state),
        )

    record = CandidateRecord(
        idempotency_key=payload.idempotency_key,
        payload_hash=digest,
        git_commit=payload.git_commit,
        model_version=payload.model_version,
        prompt_version=payload.prompt_version,
        config_version=payload.config_version,
        state=CandidateState.REGISTERED.value,
    )
    session.add(record)
    session.commit()
    session.refresh(record)

    return CandidateView(
        id=record.id,
        idempotency_key=record.idempotency_key,
        git_commit=record.git_commit,
        model_version=record.model_version,
        prompt_version=record.prompt_version,
        config_version=record.config_version,
        state=CandidateState(record.state),
    )
