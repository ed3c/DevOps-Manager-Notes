from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .contracts import CandidateCreate, CandidateState, CandidateView
from .models import CandidateRecord


class IdempotencyConflict(RuntimeError):
    pass


def _payload_hash(payload: CandidateCreate) -> str:
    body = payload.model_dump(exclude={"idempotency_key"})
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _view(record: CandidateRecord) -> CandidateView:
    return CandidateView(
        id=record.id,
        idempotency_key=record.idempotency_key,
        git_commit=record.git_commit,
        model_version=record.model_version,
        prompt_version=record.prompt_version,
        config_version=record.config_version,
        state=CandidateState(record.state),
    )


def _validate_replay(record: CandidateRecord, digest: str) -> CandidateView:
    if record.payload_hash != digest:
        raise IdempotencyConflict("idempotency key already exists with a different payload")
    return _view(record)


def register_candidate(session: Session, payload: CandidateCreate) -> CandidateView:
    digest = _payload_hash(payload)
    existing = session.scalar(
        select(CandidateRecord).where(CandidateRecord.idempotency_key == payload.idempotency_key)
    )
    if existing is not None:
        return _validate_replay(existing, digest)

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
    try:
        session.commit()
    except IntegrityError:
        # Another writer may have won the unique-key race. Re-read and admit only
        # an exact replay; any payload mismatch remains a conflict.
        session.rollback()
        winner = session.scalar(
            select(CandidateRecord).where(CandidateRecord.idempotency_key == payload.idempotency_key)
        )
        if winner is None:
            raise
        return _validate_replay(winner, digest)

    session.refresh(record)
    return _view(record)
