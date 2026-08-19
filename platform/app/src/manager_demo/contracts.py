from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class EvidenceState(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSENT = "ABSENT"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NOT_EXERCISED = "NOT_EXERCISED"
    SKIPPED_BY_POLICY = "SKIPPED_BY_POLICY"
    HUMAN_ADMIT_REQUIRED = "HUMAN_ADMIT_REQUIRED"


class EvidenceLane(StrEnum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"


class CandidateState(StrEnum):
    REGISTERED = "REGISTERED"
    EVALUATED = "EVALUATED"
    PROMOTION_ELIGIBLE = "PROMOTION_ELIGIBLE"
    REJECTED = "REJECTED"
    CANARY = "CANARY"
    PROMOTED = "PROMOTED"
    ROLLED_BACK = "ROLLED_BACK"


class SubjectIdentity(BaseModel):
    git_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    container_digest: str | None = None
    model_artifact_digest: str | None = None
    model_version: str | None = None
    prompt_version: str | None = None
    config_version: str | None = None
    eval_dataset_version: str | None = None
    eval_run_id: str | None = None
    deployment_revision: str | None = None
    kubernetes_namespace: str | None = None
    workload_or_fault_profile: str | None = None

    @field_validator("container_digest", "model_artifact_digest")
    @classmethod
    def validate_digest(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.startswith("sha256:") or len(value) != 71:
            raise ValueError("digest must be sha256:<64 hex chars>")
        int(value.removeprefix("sha256:"), 16)
        return value


class EvidenceEnvelope(BaseModel):
    schema_version: Literal["full-manager-mvp/evidence/v1"] = "full-manager-mvp/evidence/v1"
    subject: SubjectIdentity
    lane: EvidenceLane
    verdict: EvidenceState
    reason_codes: list[str] = Field(default_factory=list)


class CandidateCreate(BaseModel):
    idempotency_key: str = Field(min_length=8, max_length=128)
    git_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    model_version: str = Field(min_length=1, max_length=200)
    prompt_version: str = Field(min_length=1, max_length=200)
    config_version: str = Field(min_length=1, max_length=200)


class CandidateView(BaseModel):
    id: int
    idempotency_key: str
    git_commit: str
    model_version: str
    prompt_version: str
    config_version: str
    state: CandidateState


class BusinessOracleRequest(BaseModel):
    subject: SubjectIdentity
    expected_value: str
    observed_value: str
    force_failure: bool = False


class BusinessOracleResponse(BaseModel):
    infrastructure_http_ok: bool = True
    business_ok: bool
    evidence: EvidenceEnvelope
