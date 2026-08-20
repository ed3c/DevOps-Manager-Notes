from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import mlflow

from manager_llmops.lifecycle import CandidateIdentity, CandidateLifecycle, LifecycleState


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(dataset: dict[str, object]) -> float:
    cases = dataset["cases"]
    assert isinstance(cases, list) and cases
    correct = sum(1 for case in cases if case["expected"] == case["observed"])
    return correct / len(cases)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--workflow-commit", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    dataset_path = Path("mlops/eval/dataset-v1.json")
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    score = evaluate(dataset)
    threshold = 1.0

    identity = CandidateIdentity(
        git_commit=args.source_commit,
        model_version="qwen2.5-0.5b-candidate-unmaterialized",
        prompt_version="manager-demo-prompt-v1",
        config_version="manager-demo-config-v1",
        dataset_version=str(dataset["dataset_version"]),
        previous_good_revision="manager-demo-previous-good-v1",
    )
    lifecycle = CandidateLifecycle(identity)
    eval_state = lifecycle.apply_offline_eval(score=score, threshold=threshold)
    if eval_state != LifecycleState.PROMOTION_ELIGIBLE:
        raise SystemExit("offline evaluation unexpectedly rejected deterministic candidate")

    # Negative control: offline evaluation is perfect, but the canary/business oracle fails.
    lifecycle.start_canary()
    canary_state = lifecycle.apply_canary(business_ok=False, slo_ok=True)
    if canary_state != LifecycleState.CANARY_REJECTED:
        raise SystemExit("seeded canary/business failure was not rejected")
    rollback_target = lifecycle.rollback()

    args.workspace.mkdir(parents=True, exist_ok=True)
    mlflow_db = (args.workspace / "mlflow.db").resolve()
    artifact_root = (args.workspace / "artifacts").resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{mlflow_db}")
    experiment = mlflow.set_experiment("full-manager-mvp-public-llmops")
    with mlflow.start_run(run_name=f"public-m2-{args.source_commit[:12]}") as run:
        mlflow.set_tags({
            "source_commit": args.source_commit,
            "workflow_commit": args.workflow_commit,
            "model_version": identity.model_version,
            "prompt_version": identity.prompt_version,
            "config_version": identity.config_version,
            "dataset_version": identity.dataset_version,
            "evidence_lane": "GITHUB_HOSTED_DETERMINISTIC_MLFLOW_LIFECYCLE_ONLY",
        })
        mlflow.log_metric("offline_eval_score", score)
        mlflow.log_metric("offline_eval_threshold", threshold)
        mlflow.log_metric("canary_business_ok", 0.0)
        mlflow.log_metric("canary_slo_ok", 1.0)
        mlflow.log_dict(dataset, "eval/dataset-v1.json")
        mlflow_run_id = run.info.run_id

    receipt = {
        "schema_version": "full-manager-mvp/llmops-receipt/v1",
        "source_commit": args.source_commit,
        "workflow_commit": args.workflow_commit,
        "workflow_run_id": args.run_id,
        "mlflow": {
            "experiment_id": experiment.experiment_id,
            "run_id": mlflow_run_id,
            "tracking_backend": "local_sqlite",
        },
        "identity": {
            "model_version": identity.model_version,
            "prompt_version": identity.prompt_version,
            "config_version": identity.config_version,
            "dataset_version": identity.dataset_version,
            "dataset_sha256": sha256(dataset_path),
        },
        "offline_eval": {"score": score, "threshold": threshold, "verdict": "PASS"},
        "seeded_canary": {
            "business_ok": False,
            "slo_ok": True,
            "verdict": "REJECTED",
            "rollback_target": rollback_target,
            "final_state": lifecycle.state.value,
        },
        "checks": {
            "mlflow_run": "PASS",
            "version_identity": "PASS",
            "offline_eval_gate": "PASS",
            "offline_pass_canary_fail_negative_control": "PASS",
            "rollback_target": "PASS",
            "model_artifact_digest": "NOT_EXERCISED",
            "llama_cpp_runtime": "NOT_EXERCISED",
            "argo_rollouts_runtime": "NOT_EXERCISED",
            "production_model_traffic": "NOT_EXERCISED",
        },
        "verdict": "PASS",
        "evidence_ceiling": "GITHUB_HOSTED_DETERMINISTIC_MLFLOW_LIFECYCLE_ONLY",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
