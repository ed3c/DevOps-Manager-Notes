# Full Manager MVP Demo — Internal AI Platform

## Goal

Create a public, reviewer-runnable demo that covers the technical requirements of both target roles through one system:

- Technical Product Manager: ML/LLMOps lifecycle, platform product decisions, scaling evidence, technical communication.
- DevOps Manager: Python, Git, Docker, Kubernetes, CI/CD, automation, observability, security, incident/recovery and data-driven operations.

The demo proves only exact artifacts and runtime receipts. It cannot manufacture employment tenure, real team management, real organizational adoption, or production incident history.

## Mandatory architecture

```text
Reviewer / Demo User
        │
        ▼
React + Vite Demo Console
        │ typed API
        ▼
FastAPI + Pydantic Control Plane
        │
        ├── PostgreSQL + SQLAlchemy + Alembic
        │      lifecycle / deployment / incident / evidence state
        │
        ├── MLflow
        │      model / prompt / config / eval / registry identity
        │
        └── local LLM adapter
               llama.cpp + pinned permissive model artifact

Git commit
   ↓
GitHub Actions
   ├── pytest
   ├── Syft SBOM
   ├── Trivy vulnerability/license gate
   ├── OPA policy gate
   ├── Cosign sign/verify
   └── immutable image + evidence metadata
          ↓
       Argo CD
          ↓
    kind / Kubernetes
          ↓
    Argo Rollouts
    canary + analysis
          │
          ├── OpenTelemetry Collector
          ├── Prometheus
          └── Jaeger
                │
                ├── Locust synthetic load
                └── Toxiproxy fault injection
                       ↓
                 rollback/recovery
                       ↓
                   postmortem
                       ↓
              corrective change + re-test
                       ↓
                  evidence receipts
                       ↓
                 Demo Console / Product graph
```

## End-to-end state machine

```text
SOURCE_BOUND
→ BUILD_TESTED
→ SBOM_CREATED
→ SECURITY_POLICY_ADMITTED
→ ARTIFACT_SIGNED
→ MODEL_CONFIG_REGISTERED
→ OFFLINE_EVAL_RUNNING
    ├── EVAL_REJECTED
    └── PROMOTION_ELIGIBLE
→ GITOPS_DESIRED_STATE_BOUND
→ CANARY_RUNNING
    ├── CANARY_REJECTED → ROLLBACK_RUNNING
    └── PROMOTED
→ OBSERVED
→ LOAD_OR_FAULT_PROBE_RUNNING
→ HEALTHY | DEGRADED
→ MITIGATING
→ RECOVERED
→ POSTMORTEM_OPEN
→ CORRECTIVE_CHANGE_BOUND
→ SAME_FAILURE_RETEST
→ REVERIFIED
→ DEMO_EVIDENCE_READY
```

## Job requirement coverage

| Capability | Concrete proof | Owner |
|---|---|---|
| Python / API engineering | typed FastAPI control plane + deterministic tests | #2 |
| Git / CI/CD | exact-head GitHub Actions + immutable artifact chain | #2 |
| Docker / Kubernetes | Moby/Docker-compatible image → kind/Kubernetes | #2 |
| ML/LLM lifecycle | MLflow model/prompt/config/eval/promotion state | #7 |
| deployment / rollback | Argo CD + Argo Rollouts + known previous-good identity | #2, #7 |
| monitoring | OTel → Prometheus + Jaeger | #3 |
| 1,000-user scale evidence | 1,000 virtual-user Locust run with environment metadata | #3 |
| policy/security/license | OPA + Trivy | #4 |
| supply-chain | Syft SBOM + Cosign verification | #10 |
| failure experience | seeded bad release/model + Toxiproxy/dependency faults | #5, #10 |
| data-driven decision | SLO/business oracle + rollout threshold + incident record | #3, #5 |
| public communication | Demo Console with exact evidence/ceiling | #8 |
| final reviewer path | one documented bounded demo orchestration | #9 |

## Evidence identity

Every successful deployment/eval/incident receipt must be able to identify at least:

```text
git_commit
container_digest
model_artifact_digest_or_provider_subject
model_version
prompt_version
config_version
eval_dataset_version
eval_run_id
deployment_revision
kubernetes_namespace
rollout_revision
workload_or_fault_profile
evidence_lane
verdict
```

A UI label is not evidence. Missing identity is a failed proof obligation.

## Business oracle vs infrastructure oracle

The demo deliberately separates:

```text
readiness/liveness PASS
        ≠
request semantic/business PASS
        ≠
offline model-quality PASS
        ≠
canary business/SLO PASS
```

A seeded candidate must demonstrate a case where lower-level health remains green while the business/model oracle rejects promotion.

## Demo scenario

### Happy path

1. Register model/prompt/config candidate.
2. Run deterministic/offline eval and store result in MLflow.
3. Build image, SBOM, scan, policy-check, sign and verify.
4. Commit desired state and let Argo CD reconcile it.
5. Start Argo Rollouts canary.
6. Prometheus analysis + business oracle accept the candidate.
7. Console shows promotion and exact evidence chain.

### Failure path

1. Introduce a seeded bad prompt/config/release or a bounded Toxiproxy fault.
2. Infrastructure may remain partially healthy while model/business/SLO signal degrades.
3. Canary analysis rejects or operator initiates bounded mitigation.
4. Roll back to exact previous-good subject.
5. Record incident timeline and decision authority.
6. Apply corrective change.
7. Re-run the same planted failure.
8. Produce a new receipt showing prevention/detection.

## Local runtime policy

The deterministic CI lane must run without paid APIs. Local runtime choices are:

```text
macOS/Linux: Colima + Docker CLI/Moby
alternative: Rancher Desktop
cluster: kind
local model: llama.cpp + pinned Qwen2.5-0.5B-Instruct-GGUF candidate
```

Docker Desktop is not a required prerequisite. Its commercial terms remain outside the repo-license claims.

GPU production-shaped adapters such as vLLM/KServe are modeled separately and stay `NOT_EXERCISED` until a matching GPU/runtime receipt exists.

## License/commercial-use boundary

`registry/mvp-demo-stack.yaml` freezes the selected default stack. The default path prefers permissive licenses and avoids forced source disclosure.

Before distribution/runtime admission, also inventory:

```text
Python transitive packages
npm transitive packages
container base images
GitHub Actions / marketplace actions
Kubernetes/Argo images
MLflow/Jaeger/Prometheus images
model weights and tokenizer files
plugins/exporters
hosted/proprietary service terms if selected
```

Top-level MIT/Apache-2.0 is not a recursive legal claim.

## Molecular issue/DAG plan

```text
#11 Full MVP technology/contract freeze
   ↓ process/contract dependency
#1 invariant/evidence audit
   ↓
#2 base app + CI + container + Kubernetes
   ├── #3 observability / SLO / load
   ├── #4 policy / security / license
   ├── #7 ML/LLMOps / eval / progressive delivery
   ├── #8 Demo Console
   └── #10 SBOM / signing / bounded fault injection
           │
           ├──── verified side inputs ────┐
           ▼                              │
#5 failure / rollback / postmortem / re-test
           └───────────────┬──────────────┘
                           ▼
#9 Full Manager MVP Demo convergence
```

#3/#4/#7/#8/#10 should remain siblings when they only consume the frozen #2 contracts and own disjoint paths. If any Worker actually consumes another Worker's unmerged bytes, Tech Lead must reclassify the real branch ancestry.

## Shadow Architect checkpoints

Run mandatory review at:

```text
technology freeze
first vertical slice
first database migration
first container publish
first Kubernetes deployment
first MLflow evaluation
first canary
first green
first fault injection
first rollback
before public demo/export
```

For each checkpoint ask:

1. What became newly possible?
2. What must remain true?
3. How can we falsify it?

## Completion gate

The full demo is complete only when #9 can point to exact admitted receipts for every required lane. Otherwise the missing lane remains `NOT_IMPLEMENTED` or `NOT_EXERCISED`; documentation and UI may not fill it by assertion.
