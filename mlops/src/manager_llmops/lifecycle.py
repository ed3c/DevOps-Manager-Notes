from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class LifecycleState(StrEnum):
    CANDIDATE_REGISTERED = "CANDIDATE_REGISTERED"
    EVAL_RUNNING = "EVAL_RUNNING"
    EVAL_REJECTED = "EVAL_REJECTED"
    PROMOTION_ELIGIBLE = "PROMOTION_ELIGIBLE"
    CANARY_RUNNING = "CANARY_RUNNING"
    CANARY_REJECTED = "CANARY_REJECTED"
    PROMOTED = "PROMOTED"
    ROLLBACK_RUNNING = "ROLLBACK_RUNNING"
    ROLLED_BACK = "ROLLED_BACK"


class TransitionError(RuntimeError):
    pass


_ALLOWED: dict[LifecycleState, set[LifecycleState]] = {
    LifecycleState.CANDIDATE_REGISTERED: {LifecycleState.EVAL_RUNNING},
    LifecycleState.EVAL_RUNNING: {LifecycleState.EVAL_REJECTED, LifecycleState.PROMOTION_ELIGIBLE},
    LifecycleState.EVAL_REJECTED: set(),
    LifecycleState.PROMOTION_ELIGIBLE: {LifecycleState.CANARY_RUNNING},
    LifecycleState.CANARY_RUNNING: {LifecycleState.CANARY_REJECTED, LifecycleState.PROMOTED},
    LifecycleState.CANARY_REJECTED: {LifecycleState.ROLLBACK_RUNNING},
    LifecycleState.PROMOTED: {LifecycleState.ROLLBACK_RUNNING},
    LifecycleState.ROLLBACK_RUNNING: {LifecycleState.ROLLED_BACK},
    LifecycleState.ROLLED_BACK: set(),
}


@dataclass(frozen=True)
class CandidateIdentity:
    git_commit: str
    model_version: str
    prompt_version: str
    config_version: str
    dataset_version: str
    previous_good_revision: str

    def __post_init__(self) -> None:
        if len(self.git_commit) != 40 or any(c not in "0123456789abcdef" for c in self.git_commit):
            raise ValueError("git_commit must be a lowercase 40-char SHA")
        for field in (
            self.model_version,
            self.prompt_version,
            self.config_version,
            self.dataset_version,
            self.previous_good_revision,
        ):
            if not field:
                raise ValueError("candidate identity fields must be non-empty")


@dataclass
class CandidateLifecycle:
    identity: CandidateIdentity
    state: LifecycleState = LifecycleState.CANDIDATE_REGISTERED

    def transition(self, target: LifecycleState) -> None:
        if target not in _ALLOWED[self.state]:
            raise TransitionError(f"illegal transition: {self.state} -> {target}")
        self.state = target

    def apply_offline_eval(self, *, score: float, threshold: float) -> LifecycleState:
        self.transition(LifecycleState.EVAL_RUNNING)
        target = LifecycleState.PROMOTION_ELIGIBLE if score >= threshold else LifecycleState.EVAL_REJECTED
        self.transition(target)
        return self.state

    def start_canary(self) -> None:
        self.transition(LifecycleState.CANARY_RUNNING)

    def apply_canary(self, *, business_ok: bool, slo_ok: bool) -> LifecycleState:
        target = LifecycleState.PROMOTED if business_ok and slo_ok else LifecycleState.CANARY_REJECTED
        self.transition(target)
        return self.state

    def rollback(self) -> str:
        if self.state not in {LifecycleState.CANARY_REJECTED, LifecycleState.PROMOTED}:
            raise TransitionError(f"rollback not admitted from {self.state}")
        self.transition(LifecycleState.ROLLBACK_RUNNING)
        self.transition(LifecycleState.ROLLED_BACK)
        return self.identity.previous_good_revision
