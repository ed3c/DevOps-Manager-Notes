import pytest

from manager_llmops.lifecycle import (
    CandidateIdentity,
    CandidateLifecycle,
    LifecycleState,
    TransitionError,
)


def identity() -> CandidateIdentity:
    return CandidateIdentity(
        git_commit="a" * 40,
        model_version="model-v1",
        prompt_version="prompt-v1",
        config_version="config-v1",
        dataset_version="dataset-v1",
        previous_good_revision="good-v0",
    )


def test_offline_pass_canary_business_fail_rolls_back_exact_target() -> None:
    lifecycle = CandidateLifecycle(identity())
    assert lifecycle.apply_offline_eval(score=1.0, threshold=0.9) == LifecycleState.PROMOTION_ELIGIBLE
    lifecycle.start_canary()
    assert lifecycle.apply_canary(business_ok=False, slo_ok=True) == LifecycleState.CANARY_REJECTED
    assert lifecycle.rollback() == "good-v0"
    assert lifecycle.state == LifecycleState.ROLLED_BACK


def test_failed_offline_eval_cannot_start_canary() -> None:
    lifecycle = CandidateLifecycle(identity())
    assert lifecycle.apply_offline_eval(score=0.5, threshold=0.9) == LifecycleState.EVAL_REJECTED
    with pytest.raises(TransitionError):
        lifecycle.start_canary()


def test_candidate_cannot_promote_without_eval_and_canary() -> None:
    lifecycle = CandidateLifecycle(identity())
    with pytest.raises(TransitionError):
        lifecycle.transition(LifecycleState.PROMOTED)
