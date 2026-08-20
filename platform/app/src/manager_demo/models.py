from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .contracts import CandidateState
from .db import Base


class CandidateRecord(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    payload_hash: Mapped[str] = mapped_column(String(64))
    git_commit: Mapped[str] = mapped_column(String(40), index=True)
    model_version: Mapped[str] = mapped_column(String(200))
    prompt_version: Mapped[str] = mapped_column(String(200))
    config_version: Mapped[str] = mapped_column(String(200))
    state: Mapped[str] = mapped_column(String(40), default=CandidateState.REGISTERED.value)
