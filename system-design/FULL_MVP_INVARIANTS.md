# Full Manager MVP — Frozen Delivery & Reliability Invariants

Owner: DevOps issue #1  
Consumers: #2, #3, #4, #7, #8, #10, #5, #9  
Mode: `MONITOR`

This is the shared implementation contract for the Full Manager MVP. Downstream Workers may refine implementation details, but changing a frozen invariant requires an explicit architecture delta and a new falsifier/receipt contract.

## 1. State identity

Every state transition that can be presented to a reviewer MUST bind enough identity to reconstruct what was acted on:

```text
git_commit
container_digest or explicit no-container state
model_artifact_digest/provider subject when applicable
model_version
prompt_version
config_version
eval_dataset_version / eval_run_id when applicable
deployment_revision
kubernetes_namespace / cluster identity when applicable
workload_or_fault_profile when applicable
evidence_lane
verdict
```

`PASS` without exact identity is invalid evidence.

## 2. Business oracle is independent from infrastructure health

The following are distinct facts:

```text
process alive
!= readiness PASS
!= HTTP success
!= business-semantic correctness
!= offline model-quality PASS
!= canary/SLO promotion PASS
```

The core service MUST expose a deterministic business oracle that can fail while liveness/readiness remain healthy. A planted bad candidate MUST exercise this distinction before final convergence.

## 3. Delivery state machine

```text
SOURCE_BOUND
→ TESTED
→ ARTIFACT_BUILT
→ ARTIFACT_VERIFIED
→ DEPLOYMENT_DESIRED
→ DEPLOYMENT_OBSERVED
→ READY
→ BUSINESS_VERIFIED
→ OBSERVED

failure at any admission gate
→ REJECTED

regression after deployment
→ DEGRADED
→ MITIGATING
→ ROLLBACK_RUNNING or FORWARD_FIX_RUNNING
→ RECOVERED
```

Illegal transitions:

```text
TEST_GREEN → PRODUCTION_PROVEN
IMAGE_BUILT → IMAGE_VERIFIED
READY → BUSINESS_VERIFIED
LOCAL_K8S_PASS → PRODUCTION_CLUSTER_PROVEN
ISSUE_CLOSED → RUNTIME_CLOSED
```

## 4. Artifact immutability

A deployment MUST reference an immutable image/content identity. Mutable tags may exist for convenience but MUST NOT be the evidence subject.

Before a deployment mutates runtime state, record:

```text
candidate_subject
previous_good_subject or NO_ROLLBACK_AVAILABLE
admission_result
```

A rollback claim is invalid without a known previous-good identity and observed post-rollback verification.

## 5. Idempotency and retry

Every retried operation MUST declare whether it is idempotent.

Default retry budget for demo automation:

```text
max_attempts: 3
backoff: bounded exponential + jitter when appropriate
per_attempt_timeout: explicit
whole_operation_deadline: explicit
```

No retry loop may run indefinitely. Non-idempotent side effects MUST use an idempotency key or be rejected from automatic retry.

## 6. Resource bounds

The MVP MUST bound or observe saturation for:

```text
CPU
memory
request concurrency
DB connection pool
queue depth, if introduced
retry count
subprocess count
subprocess stdout/stderr
load-test duration
fault-injection duration
cluster namespace/resources created by the demo
```

Initial Kubernetes resource requests/limits are implementation inputs, not performance claims. Missing limits require an explicit exception in the receipt.

## 7. Demo SLO contract

These are **demo acceptance targets**, not production SLO claims.

Control-plane business endpoint, under the declared deterministic load profile:

```text
availability_window: 10 minutes steady-state when the local host can support the profile
business_success_ratio_target: >= 0.99
server_error_ratio_target: <= 0.01
p95_latency_target: <= 1.0 second for the non-LLM control-plane business path
no_progress_timeout: 30 seconds
```

The local LLM inference path MUST have a separate latency profile and MUST NOT be judged by the non-LLM p95 target.

A 1,000 virtual-user run is a synthetic capacity experiment. If the admitted host cannot sustain 1,000 VU, the result is still recorded as a bounded capacity finding; it is never silently skipped or rewritten as PASS.

## 8. Availability and failure observability

The runtime/evidence model MUST distinguish at least:

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
TIMEOUT
PARTIAL
UNKNOWN
HUMAN_ADMIT_REQUIRED
```

If the canonical evidence enum remains narrower, timeout/partial/unknown MUST be carried as reason codes under a non-PASS state rather than collapsed to PASS.

## 9. Database and migration invariants

PostgreSQL is durable control-plane state for the Full MVP. Alembic migration work MUST satisfy:

```text
schema revision identity is recorded
forward migration is deterministic for the supported starting revision
rollback capability is explicit: reversible or deliberately irreversible
an irreversible migration cannot be auto-admitted without a compensating recovery plan
application startup against an incompatible schema fails closed
```

Backup/restore is not proven until an actual bounded restore drill executes.

## 10. Kubernetes / GitOps invariants

Local Kubernetes evidence MUST record cluster/tool version and namespace identity.

Desired vs observed state MUST be distinguishable. Argo CD reconciliation and Argo Rollouts promotion are separate state machines.

No deployment is considered verified solely because Kubernetes reports a Ready pod. Business verification is a separate gate.

Cleanup MUST be bounded and target only demo-owned namespace/resources.

## 11. ML/LLMOps invariants

For issue #7:

```text
registered candidate
!= evaluated candidate
!= promotion-eligible candidate
!= canary candidate
!= promoted candidate
```

Offline evaluation threshold, evaluation dataset identity and MLflow run identity MUST be recorded.

A candidate can pass offline evaluation and still fail canary/business verification. The Full MVP MUST include this negative case.

Model weight/license/digest is a separate subject from the llama.cpp runtime license.

## 12. Observability invariants

A request/candidate/deployment identity MUST be correlatable across the evidence path where technically feasible.

At minimum expose:

```text
request count
business success/failure count
server error count
latency histogram/quantiles derived from histogram data
active deployment revision
candidate/promotion state
```

Telemetry loss is a distinct failure. Missing telemetry cannot be interpreted as healthy.

## 13. Security and supply-chain invariants

The exact immutable artifact subject must flow through:

```text
SBOM generation
vulnerability/license scan
policy evaluation
signature/signature verification
```

A planted unsigned/mismatched artifact and at least one policy violation MUST be rejected.

Secrets, credentials and private tokens MUST NOT be committed into source, receipts or Demo Console payloads.

Top-level project license never recursively clears transitive dependencies, images, plugins, model artifacts or SaaS terms.

## 14. Fault-injection invariants

Faults are bounded `DRILL` / `SIMULATION` only.

Every fault packet declares:

```text
target
fault type
start condition
maximum duration
expected oracle
cleanup command/operation
cleanup verification
```

A fault without a bounded cleanup path is blocked.

## 15. Recovery closure

A Manager-grade failure loop closes only through:

```text
trigger
→ detection
→ decision authority
→ mitigation
→ recovery
→ postmortem
→ corrective change
→ same-failure re-test
→ exact receipt
```

Recovery success MUST re-run the business oracle, not only infrastructure readiness.

## 16. Authority

Unattended Workers MAY prepare reversible code/docs/tests and bounded local demo operations admitted by a typed task packet.

Human/trusted-owner authority remains required for:

```text
semantic conflict resolution
force push
merge/release
repository visibility or permission widening
production promotion/rollback admission
credential/provider enrollment
claims of real users, production incidents, production infrastructure tenure or people-management tenure
```

## 17. Evidence ceilings

```text
L0 SOURCE_CLAIM
L1 STATIC_REASONING
L2 DETERMINISTIC_TEST
L3 LOCAL_INTEGRATION
L4 REAL_SUBSTRATE
L5 ADVERSARIAL_OR_CHAOS
L6 PRODUCTION_OBSERVATION
```

A lower lane never self-promotes. The Full MVP is expected to reach L2-L5 across different subclaims; it is not expected to manufacture L6 production evidence.

## 18. Shadow Architect checkpoints

Mandatory review checkpoints:

```text
invariant freeze
first schema migration
first immutable artifact
first Kubernetes deployment
first external/process integration
first MLflow evaluation
first canary
FIRST_GREEN
first synthetic 1000-VU attempt
first fault injection
first rollback/recovery
before final public demo convergence
```

For each checkpoint record:

```text
delta class
what became newly possible
what must remain true
falsifier/oracle
intervention L0-L3
evidence impact
```

## #2 admission gate

Issue #2 may begin implementation after this invariant contract and issue #1 evidence audit are committed on an exact child branch. Issue #2 may reach deterministic FIRST_GREEN remotely; Docker/kind/Kubernetes execution remains Local Handoff unless an admitted runtime is available in-session.
