# AGENTS.md

## Purpose

This public repository is the executable evidence plane for the Full Manager MVP Demo. It must remain independently reviewable and public-safe.

`Product-Manager-Notes` is the public-safe Manager requirement/routing/narrative plane. `skills-shared` owns reusable Tech Lead, Shadow Architect and Git Town procedures. This repository owns implementation, CI/runtime/failure evidence, exact receipts, the Demo Console, reviewer convergence and typed Local Handoff.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md`
5. `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md`
6. `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md`
7. `docs/milestones/PUBLIC_M5_LOCAL_KIND_RUNNER_READY.md`
8. `roles/devops-manager/job-contract.yaml`
9. `registry/mvp-demo-stack.yaml`
10. `registry/evidence.yaml`
11. `registry/gaps.yaml`
12. `registry/stack-plan.yaml`
13. `registry/public-m2-first-green.json`
14. `registry/public-m3-failure-recovery.json`
15. `registry/public-m4-reviewer-convergence.json`
16. `registry/public-m5-local-kind-readiness.json`
17. `handoff/local-handoff-queue.json` when crossing the local/runtime boundary
18. exact issue / PR / commit / Actions run / artifact / receipt
19. nearest directory README/contract/test/receipt

Reusable method is read from canonical `ed3c/skills-shared` owners, not copied into consumer variants:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Trigger-selected support only:

```text
runtime-env                secret-free runtime/profile/workload contracts
truth-verify-loop          mutable/high-risk external claim verification
openwiki-source-anchoring  exact source/path/quote anchoring
skill-resume-site          admitted public portfolio projection only
```

No support repository becomes a second mutable authority for this repo.

## Operating mode

Default `MODE=MONITOR`.

Builder may perform reversible design/code/tests and bounded execution. Shadow Architect independently watches:

```text
ASSUMPTION_DELTA
STATE_DELTA
AUTHORITY_DELTA
OWNERSHIP_DELTA
LIFECYCLE_DELTA
CONCURRENCY_DELTA
RESOURCE_DELTA
EXTERNAL_SIDE_EFFECT_DELTA
FAILURE_SURFACE_DELTA
EVIDENCE_DELTA
```

For every material delta ask:

1. What became newly possible?
2. What must now remain true?
3. How would we know it is false?

Intervention:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

L3 includes unsafe/irreversible change, secret/private disclosure, destructive migration without rollback, privilege expansion, unbounded fault injection, overlapping mutation authority, semantic conflict, failed cleanup, evidence laundering or public claim inflation.

## Current checkpoints

```text
M1 CORE_REMOTE_FIRST_GREEN                         PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN      PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN  PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY         PASS_BOUNDED
```

M5 means the local kind/Kubernetes runner and its queue contract are concrete and safety-reviewed. It does **not** mean the local command ran.

Exact M5 subjects:

```text
PR #51 runner
  head 20d2ccb0ed8c877309452eece7c755bb3411c4c1
  tree 7d4b5d5aaba2d023803b152ce5ac7f23f274eba0
  CI   32259961112 PASS
  ceiling GITHUB_HOSTED_LOCAL_RUNNER_CONTRACT_ONLY

PR #52 queue
  head 660d4deea81712f3d6ab5288ae09288b2e15cc27
  CI   32260403160 PASS
  ceiling GITHUB_HOSTED_LOCAL_HANDOFF_CONTRACT_VALIDATION_ONLY
```

Local runtime receipts are still absent.

## Eight-stage contract

```text
P0 SUBJECT_AUTHORITY
→ P1 SOURCE_EVIDENCE
→ P2 PROBLEM_CLOSURE_SYSTEM_DESIGN
→ P3 TECHNOLOGY_ADR
→ P4 TECH_LEAD_STACK_PLAN
→ P5 PARALLEL_IMPLEMENTATION
→ P6 SHADOW_RUNTIME_FAILURE
→ P7 CONVERGENCE_HANDOFF
```

Start-readiness and completion-readiness are different edge classes. A task may start with bounded unknowns but cannot close without its own receipt and completion predecessors.

Every zero-context handoff records:

```text
repository / branch / commit / tree / issue
state_in / state_out
goal / non-goals
allowed / read-only / forbidden paths
resource leases
consumed / produced artifacts
start / completion dependencies
invariants / negative controls
evidence state / ceiling
Shadow deltas / intervention
unknowns / blockers
Local Handoff requirement
next prompt / stage
Human-owned operations
```

## Tech Lead laws

- Freeze exact subject, objective, non-goals, invariants, dependencies, acceptance criteria, budgets, rollback and evidence lane before fan-out.
- Dependencies require real artifact/state consumption or an admitted receipt.
- Git ancestry and task DAG are separate graphs.
- Parallel writers require disjoint path/resource leases; record observed lease deltas.
- Worker/LLM/issue/branch/process/CI self-report is candidate evidence only.
- Every deployment side effect has rollback/reconciliation semantics.
- Retry paths require idempotency and bounded retry budgets.
- Growing resources require bounds or saturation oracles.
- Performance claims name workload/environment/window/duration/evidence lane.
- FIRST_GREEN triggers Shadow review; it does not close production proof.
- Synthetic incidents remain `DRILL`/`SIMULATION`.
- 1,000 virtual users are synthetic load evidence, not 1,000 real users.
- Local Kubernetes is not production-cluster experience.
- UI state cannot promote backend evidence.
- Queue existence cannot promote queue execution.
- Runner-contract CI cannot promote physical/local runtime state.

## Evidence subject law

Mutable routing subjects and historical evidence subjects are distinct:

```text
current_head
  current PR/branch routing identity

evidence_head
  exact commit that produced an admitted artifact
```

Never relabel an older artifact as evidence for a newer head.

## Molecular Git Town laws

Follow `git-town-stacked-pr-worker`:

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical/local prerequisite             → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Observed execution ancestry:

```text
PR #14 Core
├─ PR #36 Observability
├─ PR #38 Policy/Security
├─ PR #39 ML/LLMOps
├─ PR #37 Demo Console
└─ PR #40 Supply/Fault

PR #36
└─ PR #42 Failure/Recovery
     ↑ exact side evidence #38/#39/#40

PR #42
└─ PR #44 Reviewer Convergence
     ↑ exact Demo Console bytes #37 + M2/M3 artifacts
     └─ PR #45 M4 Local Handoff
          └─ PR #51 M5 Live-kind Runner
               └─ PR #52 M5 Queue Compiler
```

Never fabricate multi-parent Git history. A convergence owner has one real Git base and typed side inputs.

## M4 reviewer laws

Issue #9 / PR #44 uses two distinct remote proof lanes:

```text
full-reviewer-demo.yml
→ exact Demo Console byte parity
→ current PR-head readback
→ deterministic reviewer bootstrap
→ seven DRILL replays
→ business PASS/FAIL telemetry

full-reviewer-convergence.yml
→ six exact Actions artifact re-downloads
→ archive SHA-256 verification
→ required-path admission
→ bounded reviewer bundle
```

Their evidence ceilings remain separate.

Deterministic reviewer entrypoint:

```bash
bash scripts/demo/run_reviewer_demo.sh <output-directory>
```

This has no paid model/provider API dependency, but it is not live-substrate proof.

## M5 Local Handoff laws

The canonical queue is `handoff/local-handoff-queue.json`.

Current state:

```text
M4-LOCAL-REVIEWER-001       ACTIVE
M4-LIVE-SUBSTRATE-002       WAITING_PREDECESSOR
M5-ARGO-MODEL-CAPACITY-003  BLOCKED_UNRESOLVED
```

### Current ACTIVE item

```bash
bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
```

Expected receipt:

```text
evidence/local-reviewer/reviewer-demo-receipt.json
verdict PASS_BOUNDED
ceiling LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY
```

Until this receipt exists and passes, **do not execute the live-kind item**.

### Concrete live-kind item

Runner subject:

```text
PR #51
commit 20d2ccb0ed8c877309452eece7c755bb3411c4c1
tree   7d4b5d5aaba2d023803b152ce5ac7f23f274eba0
```

Required local artifact identity input:

```text
M5_KIND_NODE_IMAGE=<exact-name>@sha256:<64-lowercase-hex>
```

Command after predecessor admission:

```bash
bash scripts/handoff/run_live_kind_from_env.sh \
  --output evidence/local-kind/local-kind-receipt.json \
  --cluster-name manager-demo-m5 \
  --local-port 18030
```

The runner:

- refuses cluster names outside `manager-demo-*`;
- refuses takeover of a pre-existing target cluster;
- creates at most one cluster;
- binds one exact OCI descriptor digest;
- uses the existing bounded two-replica CPU/memory K8s contract;
- proves liveness/readiness separately from business PASS/forced FAIL;
- captures pod runtime image IDs;
- treats partial `kind create` as owned for cleanup;
- terminates port-forward, deletes the attempted cluster and temporary files;
- restores caller kubectl current-context when one existed.

A real PASS can reach only:

```text
LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

It cannot prove Argo runtime, model runtime, 1,000-VU behavior or production tenure.

### Advanced item

`M5-ARGO-MODEL-CAPACITY-003` remains `BLOCKED_UNRESOLVED` and has no command. Do not activate it until exact Argo CD/Rollouts image/tool subjects, exact Qwen revision/file/digest/license, exact llama.cpp build/binary and 1,000-VU host budgets/abort thresholds/cleanup are committed.

## Local Handoff schema law

Every ACTIVE executable item binds:

```text
exact target commit + tree
required capabilities
concrete argv + cwd + timeout
environment names, never secret values
resource budget
sanitized durable receipt
required PASS exit
cleanup obligation
next item only when its runner exists
```

Do not put credentials, arbitrary shell strings, private reasoning or fabricated future commands into a queue.

## Evidence states / ladder

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

```text
L0 SOURCE_CLAIM
L1 STATIC_REASONING
L2 DETERMINISTIC_TEST
L3 LOCAL_INTEGRATION
L4 REAL_SUBSTRATE
L5 ADVERSARIAL_OR_CHAOS
L6 PRODUCTION_OBSERVATION
```

Lower evidence never self-promotes.

Forbidden promotions:

```text
CI_GREEN               → BUSINESS_CORRECT
REMOTE_FIRST_GREEN     → PRODUCTION_RUNTIME
RUNNER_CONTRACT_PASS   → LOCAL_KIND_PASS
QUEUE_CONTRACT_PASS    → QUEUE_EXECUTED
LOCAL_REVIEWER_PASS    → LIVE_KIND_PASS
LOCAL_K8S_PASS         → PRODUCTION_INFRA_EXPERIENCE
1000_VU_PASS           → 1000_REAL_USERS
DRILL_COMPLETE         → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS  → BLANKET_LEGAL_CLEARANCE
UI_GREEN               → BACKEND_EVIDENCE_PASS
CURRENT_PR_HEAD         → HISTORICAL_ARTIFACT_EVIDENCE
```

## Technology admission

`registry/mvp-demo-stack.yaml` is the selected stack inventory. Default distribution prefers permissive families; top-level license identity is not recursive clearance.

Separate subjects include Python/npm transitives, container images, K8s/Argo/MLflow/Jaeger/Prometheus images, plugins, Actions, model weights/tokenizers and hosted service terms. Every downloaded model/image/tool artifact requires digest + license record before admission.

## Public disclosure / Google boundary

GitHub is canonical for public executable evidence. Google Doc/Sheet are non-authoritative human mirrors. Public code/evidence must not contain credentials, private customer/user data, employer/client confidential material, private source bodies or restricted redistribution material.

## Automation boundary

Unattended workers may update bounded code/docs/tests, run deterministic CI, emit candidate receipts and prepare draft PRs. Stop on:

```text
stale/wrong subject
overlapping writer/resource lease
missing predecessor receipt
semantic conflict
required local capability unavailable
secret/private disclosure risk
unbounded side effect/resource/fault
invalid receipt
failed cleanup
Human-owned transition
```

Human/trusted-owner operations:

```text
semantic conflict resolution
force push / merge / release
repository visibility / permission changes
production promotion / rollback admission
credential/provider enrollment
claims of real users, real incidents, production tenure or people-management tenure
```
