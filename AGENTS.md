# AGENTS.md

## Purpose

This public repository is the executable evidence plane for the Full Manager MVP Demo. It must remain independently reviewable, public-safe and explicit about evidence ceilings.

`Product-Manager-Notes` owns public-safe requirements/routing/narrative state. `skills-shared` owns reusable Tech Lead, Shadow Architect and Git Town procedures. This repository owns implementation, deterministic/runtime/failure evidence, exact receipts, reviewer convergence, bounded runtime runners and typed Local Handoff contracts.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_M7_ADVANCED_EXECUTION_BUNDLE_READY.md`
5. `registry/public-m7-advanced-bundle.json`
6. `registry/stack-plan.yaml`
7. `registry/mvp-demo-stack.yaml`
8. `registry/evidence.yaml`
9. `registry/gaps.yaml`
10. `handoff/local-handoff-queue.json` before any physical/local continuation
11. exact issue / PR / current head / evidence head / Actions run / artifact / receipt
12. nearest directory README/contract/test/receipt

For prior checkpoints, traverse M2 → M3 → M4 → M5 → M6 from `docs/INDEX.md`.

Canonical reusable methods are read from `ed3c/skills-shared`; never fork local procedural variants:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Current canonical Local Handoff method subject:

```text
ed3c/skills-shared@4ca9417b1da5ff32f1d4d3e7af64a15908749024
schema:    agentic-tech-lead/local-handoff-queue/v1
assertion: skills/agentic-tech-lead-orchestration/scripts/assert_local_handoff_queue.py
```

A consumer queue is not admitted unless the portable assertion and its negative-control selftest pass.

## Operating mode

Default `MODE=MONITOR`.

Builder may perform reversible design/code/tests and bounded remote execution. Shadow Architect independently watches:

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
CONTRACT_DRIFT
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

L3 includes unsafe/irreversible mutation, secrets/private disclosure, authority widening, unbounded load/fault/download/resource behavior, overlapping mutation ownership, semantic conflict, failed cleanup, stale subject admission, fixture/live evidence laundering or public claim inflation.

## Current checkpoints

```text
M1 CORE_REMOTE_FIRST_GREEN                          PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                 PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN       PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN   PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY          PASS_BOUNDED
M6 PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY            PASS_BOUNDED
M7 PUBLIC_ADVANCED_EXECUTION_BUNDLE_READY             PASS_BOUNDED
```

M7 proves the converged runner-bundle / receipt-gated queue-compiler contract. It does **not** prove physical local execution.

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

Start-readiness and completion-readiness are separate edge classes. A readable parent contract can make work startable; only an identity-matched receipt in the owning evidence lane can make a completion edge closed.

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

- Freeze exact subject, objective, non-goals, invariants, dependencies, acceptance criteria, resource budgets, cleanup/rollback and evidence lane before fan-out.
- A dependency exists only for real artifact/state consumption or an admitted completion receipt.
- Git ancestry and task/process DAG are separate graphs.
- Parallel writers require disjoint path/resource leases; record any observed lease delta.
- Worker/LLM/issue/branch/process/CI self-report is candidate evidence only.
- Every deployment/runtime side effect requires cleanup, rollback or reconciliation semantics.
- Retry requires idempotency and a bounded retry budget.
- Every growing resource or external download requires a bound or saturation oracle.
- Performance claims name workload, environment, duration/window and evidence lane.
- FIRST_GREEN triggers Shadow review; it does not close production proof.
- Synthetic incidents remain `DRILL`/`SIMULATION`.
- 1,000 VU is synthetic load evidence, never 1,000 real users.
- Local Kubernetes is not production-cluster experience.
- Queue/runner/compiler contract PASS is not physical execution PASS.
- Fixture PASS cannot satisfy a live predecessor receipt.
- UI, docs, issue state or PR state cannot promote backend/runtime evidence.

## Evidence subject law

Mutable routing and admitted historical evidence are distinct:

```text
current_head   mutable PR/branch routing identity
evidence_head  exact commit that produced admitted evidence
```

Never relabel an older artifact/run as evidence for a newer head. A later correction may supersede the routing subject while the older run remains historical evidence only.

## Molecular Git Town laws

Follow `git-town-stacked-pr-worker`:

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical/local prerequisite             → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Observed implementation ancestry:

```text
PR #14 Core
├─ PR #36 Observability
├─ PR #38 Policy/Security
├─ PR #39 ML/LLMOps
├─ PR #37 Demo Console
└─ PR #40 Supply/Fault

PR #36 → PR #42 Failure/Recovery
PR #42 → PR #44 Reviewer Convergence → PR #45 → PR #51 → PR #52

M6 task siblings with real Git parents:
PR #39 → PR #55 Argo
PR #39 → PR #56 Model
PR #36 → PR #57 Capacity
PR #40 → PR #58 Registry Signing

M7 convergence:
PR #52 → PR #65 Advanced Execution Bundle
             ↑ exact runner-byte side inputs #55/#56/#57/#58
```

PR #65 has one real Git parent. Do not fabricate a multi-parent Git merge merely because it converges four task inputs.

## Canonical current Local Handoff

Shadow previously found consumer/schema drift in the first queue. PR #52 is the canonical current queue contract:

```text
PR #52 current head
  f7a3937d7d0979e3adfaf1ebc4adc0532450d925

execution epoch
  commit   4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
  tree     5ff3349c1eb5c7976263c2e89347a353ccbc1072
  rollback 660d4deea81712f3d6ab5288ae09288b2e15cc27

contract workflow
  32263239722 PASS
```

Current physical queue:

```text
M5-LOCAL-REVIEWER-001       ACTIVE
M5-LIVE-KIND-002            BLOCKED_BY_PREDECESSOR
M6-ADVANCED-SUBSTRATE-003   BLOCKED_BY_PREDECESSOR
```

No Agent may skip this predecessor chain because a newer runner/compiler exists.

## M6 runner contracts — exact current subjects

```text
PR #55 Argo
  head 8d976171f4aa2eba72bee360823b660f9bed99d4
  tree fada58f36c83de296decb41dcd34531b9d73145a
  run  32274548200 PASS
  contract ceiling GITHUB_HOSTED_ARGO_RUNNER_CONTRACT_ONLY
  future real ceiling LOCAL_ARGO_CONTROLLERS_READY_ONLY

PR #56 Model
  head 63355992f382cf260c624e2c7c7c3733cce82c20
  run  32265971683 PASS
  future real ceiling LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY

PR #57 Capacity
  head 2240e8ee7ae9f151503d5c03d8043938dbbdce95
  run  32266078175 PASS
  future real ceiling LOCAL_SYNTHETIC_1000_VU_ONLY

PR #58 Registry Signing
  head 1b543fdfad73377fa6ba51e3f190b56ed60452fa
  run  32266026763 PASS
  future real ceiling LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY
```

The earlier PR #55 subject `284dbf1d...` remains historical contract evidence; do not use it as current Argo runner identity.

### Argo lifecycle law

M7 exposed a real lifecycle mismatch: M5 live-kind cleanup deletes its cluster, so advanced Argo cannot assume the predecessor cluster survives. The current PR #55 adds self-contained ephemeral-kind ownership:

```text
exact kind node image digest
→ refuse pre-existing manager-demo-* cluster
→ capture caller kubectl context
→ create one bounded ephemeral kind cluster
→ execute exact Argo controller runner
→ require inner receipt + cleanup PASS
→ delete attempted cluster
→ restore caller context
```

Controller readiness is still not Argo CD Application reconciliation or live Rollouts canary evidence.

### Model law

- exact llama.cpp 40-hex commit + model HTTPS URL + SHA-256 + admitted license ID required;
- Qwen demo lane license ID is `Apache-2.0`; source metadata never invents revision/file/digest;
- model download <=2 GB, build parallelism <=2, threads <=8, tokens <=128, runtime <=300 s;
- source/build/model bytes are temporary and cleanup-owned.

### Capacity law

- loopback only, occupied-port refusal;
- <=1,000 VU, spawn <=100/s, duration <=60s;
- temporary venv and no persistent pip cache;
- aggregate request count, p95 and failure-ratio gates required.

### Registry-signing law

- exact registry image digest and exact cosign binary SHA-256 required;
- one loopback registry, one image build/push/signature, ephemeral local keypair;
- no external registry credentials;
- local image, registry container and key/temp material cleanup-owned.

## M7 advanced execution bundle

Issue #60 / PR #65 owns convergence.

```text
PR #65
  head cf63e2fc85d56c2e49cfefd33fefbec30316e1fa
  tree 7dce94e01dd3630662deb6dfb3c67c8b5f272bb0
  run  32275551599 PASS
  ceiling GITHUB_HOSTED_M7_ADVANCED_BUNDLE_AND_QUEUE_COMPILER_ONLY
```

CI requirements:

```text
exact runner byte parity #55/#56/#57/#58        PASS
compiler/runners compile                         PASS
predecessor receipt controls                     7/7 PASS
fixture one-ACTIVE queue                         PASS
portable Local Handoff assertion                 PASS
portable Local Handoff selftest                  PASS
fixture physical_runtime_executed=false          PASS
```

Intermediate red runs `32275347591` and `32275449122` remain non-admitted evidence. They were corrected without weakening the runtime contract.

### Live predecessor admission

`compile_m7_advanced_queue.py` may compile a live advanced queue only from the canonical PR #52 execution epoch and these live receipts:

```text
reviewer receipt
  schema   full-manager-mvp/local-reviewer-handoff-receipt/v1
  state    PASS
  ceiling  LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY

kind receipt
  schema   full-manager-mvp/local-kind-substrate-receipt/v1
  verdict  PASS
  ceiling  LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

Wrong/absent/FAIL/wrong-subject/wrong-ceiling receipts fail closed.

### Fixture law

Fixtures exist only under `tests/handoff/fixtures/m7/` and declare:

```text
evidence_kind = FIXTURE
```

They are legal only with explicit `--fixture-mode`. Fixture compilation must record:

```text
evidence_kind             FIXTURE
physical_runtime_executed false
evidence_ceiling          FIXTURE_COMPILER_CONTRACT_ONLY
```

Fixture receipts can validate compiler topology, never live state advancement.

### Future advanced queue order

When both real predecessor receipts are eventually admitted, the compiler produces exactly one ACTIVE item:

```text
M7-ARGO-CONTROLLERS-001       ACTIVE
        ↓ exact PASS receipt + cleanup
M7-LOCAL-MODEL-002            BLOCKED_BY_PREDECESSOR
        ↓ exact PASS receipt + cleanup
M7-CAPACITY-003               BLOCKED_BY_PREDECESSOR
        ↓ exact PASS receipt + cleanup
M7-REGISTRY-SIGNING-004       BLOCKED_BY_PREDECESSOR
```

Sequential order is deliberate: local cluster/model/load/registry resource ownership must not overlap.

## Evidence states and ladder

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

Forbidden promotions include:

```text
CI_GREEN                → BUSINESS_CORRECT
RUNNER_CONTRACT_PASS    → PHYSICAL_RUNTIME_PASS
QUEUE_COMPILER_PASS     → QUEUE_EXECUTED
FIXTURE_PASS            → LIVE_PREDECESSOR_PASS
LOCAL_K8S_PASS          → PRODUCTION_INFRA_EXPERIENCE
ARGO_CONTROLLERS_PASS   → APPLICATION_RECONCILIATION_PASS
LOCAL_MODEL_PASS        → PRODUCTION_LLM_TRAFFIC
1000_VU_PASS            → 1000_REAL_USERS
LOCAL_SIGNING_PASS      → PRODUCTION_KEY_CUSTODY
DRILL_COMPLETE          → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS   → BLANKET_LEGAL_CLEARANCE
CURRENT_PR_HEAD         → HISTORICAL_ARTIFACT_EVIDENCE
```

## Automation boundary

Unattended workers may create/update bounded public-safe code/docs/tests, run deterministic CI, emit candidate receipts and prepare draft PRs when contracts allow it.

Stop on:

```text
stale/wrong exact subject
overlapping writer/resource lease
missing completion receipt
semantic conflict
physical capability unavailable
secret/private disclosure risk
unbounded retry/resource/download/load/fault behavior
invalid/mismatched receipt
failed cleanup
canonical method/schema drift
Human-owned transition
```

Human/trusted-owner operations:

```text
merge / force-push / release
issue closure when used as authority transition
repository visibility / permission widening
production promotion / rollback admission
credential/provider enrollment
semantic-conflict resolution
claims of real users, real incidents, production tenure or people-management tenure
```

## Next legal frontier

```text
M7 bundle/compiler contract             PASS_BOUNDED
        ↓
M5-LOCAL-REVIEWER-001                   real PASS receipt required
        ↓
M5-LIVE-KIND-002                        real PASS receipt required
        ↓
compile M7 advanced queue in live mode
        ↓
M7-ARGO-CONTROLLERS-001
→ M7-LOCAL-MODEL-002
→ M7-CAPACITY-003
→ M7-REGISTRY-SIGNING-004
```

Until real predecessor receipts exist, all physical local reviewer/kind/Argo/model/1,000-VU/signing evidence remains `NOT_EXERCISED`.
