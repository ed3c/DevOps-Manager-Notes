# AGENTS.md

## Purpose

This public repository is the executable evidence plane for the Full Manager MVP Demo. It must remain independently reviewable and public-safe.

`Product-Manager-Notes` owns public-safe requirements/routing/narrative state. `skills-shared` owns reusable Tech Lead, Shadow Architect and Git Town procedures. This repository owns implementation, CI/runtime/failure evidence, exact receipts, reviewer convergence and typed Local Handoff contracts.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_M6_ADVANCED_RUNNER_CONTRACTS_READY.md`
5. `registry/public-m6-runner-contracts.json`
6. `registry/stack-plan.yaml`
7. `registry/mvp-demo-stack.yaml`
8. `registry/evidence.yaml`
9. `registry/gaps.yaml`
10. `handoff/local-handoff-queue.json` when crossing the physical/local boundary
11. exact issue / PR / current head / evidence head / Actions run / artifact / receipt
12. nearest directory README/contract/test/receipt

For prior checkpoints, traverse M2 → M3 → M4 → M5 from `docs/INDEX.md`.

Canonical reusable methods are read from `ed3c/skills-shared`; do not fork local procedural variants:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Current canonical method subject for Local Handoff:

```text
ed3c/skills-shared@4ca9417b1da5ff32f1d4d3e7af64a15908749024
schema: agentic-tech-lead/local-handoff-queue/v1
assertion: skills/agentic-tech-lead-orchestration/scripts/assert_local_handoff_queue.py
```

A consumer queue is not admitted unless the portable assertion and its negative-control selftest pass.

## Operating mode

Default `MODE=MONITOR`.

Builder may perform reversible design, code, tests and bounded remote execution. Shadow Architect independently watches:

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

L3 includes irreversible/destructive behavior without rollback, secrets/private disclosure, permission expansion, unbounded fault/load/resource activity, overlapping writer/resource authority, semantic conflict, failed cleanup, evidence laundering, stale exact subjects or public claim inflation.

## Current checkpoints

```text
M1 CORE_REMOTE_FIRST_GREEN                          PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                 PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN       PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN   PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY          PASS_BOUNDED
M6 PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY            PASS_BOUNDED
```

M6 means the public runner contracts exist and passed contract-only CI. It does not mean any physical M6 runner executed.

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

Start-readiness and completion-readiness are separate edge classes. A task may start with bounded unknowns but cannot close without its own exact receipt and all completion predecessors.

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
- A dependency edge exists only for real artifact/state consumption or an admitted completion receipt.
- Git ancestry and task-DAG dependencies are separate graphs.
- Parallel writers require disjoint file/resource leases; record any observed lease delta.
- Worker/LLM/issue/branch/process/CI self-report is candidate evidence only.
- Every deployment/runtime side effect has cleanup, rollback or reconciliation semantics.
- Retry paths require idempotency and bounded retry budgets.
- Every growing resource or external download has a bound or saturation oracle.
- Performance claims name workload, environment, window/duration and evidence lane.
- FIRST_GREEN triggers Shadow review; it does not close production proof.
- Synthetic incidents remain `DRILL`/`SIMULATION`.
- 1,000 virtual users are synthetic load evidence, not 1,000 real users.
- Local Kubernetes is not production-cluster experience.
- Queue/runner contract PASS is not physical execution PASS.
- UI or documentation cannot promote backend/runtime evidence.

## Evidence subject law

Mutable routing subjects and historical evidence subjects are distinct:

```text
current_head
  current PR/branch routing identity

evidence_head
  exact commit that produced an admitted artifact
```

Never relabel an older Actions artifact as evidence for a newer head.

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
PR #39 → PR #55 Argo contract
PR #39 → PR #56 model contract
PR #36 → PR #57 capacity contract
PR #40 → PR #58 registry-signing contract
```

Do not fabricate one common Git parent merely because four M6 tasks share one program milestone.

## Canonical Local Handoff law

Shadow Architect found consumer/schema drift in the first M5 queue. The corrected PR #52 must be treated as canonical:

```text
current PR #52 head
  f7a3937d7d0979e3adfaf1ebc4adc0532450d925

canonical execution epoch
  commit   4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
  tree     5ff3349c1eb5c7976263c2e89347a353ccbc1072
  rollback 660d4deea81712f3d6ab5288ae09288b2e15cc27

workflow
  Canonical Local Handoff contract / run 32263239722 / PASS
```

The queue uses only the portable schema vocabulary:

```text
states:
  ACTIVE
  BLOCKED_BY_PREDECESSOR
  COMPLETE

runtime classes:
  LOCAL_RUNTIME
  LOCAL_PROVIDER
  LOCAL_FORGE
  LOCAL_HOST
  MIXED
```

Automation-forbidden tokens include at least:

```text
merge
force_push
issue_close
queue_advance
provider_activation
semantic_conflict_resolution
```

Every item in one queue epoch binds the same root execution-subject commit. Live exits require a durable `PASS` receipt. Queue advancement is not performed by an unattended worker merely because predecessor tests look green.

Current queue:

```text
M5-LOCAL-REVIEWER-001       ACTIVE
M5-LIVE-KIND-002            BLOCKED_BY_PREDECESSOR
M6-ADVANCED-SUBSTRATE-003   BLOCKED_BY_PREDECESSOR
```

## M6 runner contracts

Issue #54 owns the program-level runner-contract fan-out. Exact subjects:

```text
PR #55 Argo controller contract
  head 284dbf1d2e9a1759cab0a8cb21987f76112946b5
  run  32265921102 PASS
  contract ceiling GITHUB_HOSTED_ARGO_RUNNER_CONTRACT_ONLY
  future real ceiling LOCAL_ARGO_CONTROLLERS_READY_ONLY

PR #56 local model contract
  head 63355992f382cf260c624e2c7c7c3733cce82c20
  run  32265971683 PASS
  contract ceiling GITHUB_HOSTED_LOCAL_MODEL_RUNNER_CONTRACT_ONLY
  future real ceiling LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY

PR #57 1,000-VU contract
  head 2240e8ee7ae9f151503d5c03d8043938dbbdce95
  run  32266078175 PASS
  contract ceiling GITHUB_HOSTED_1000_VU_RUNNER_CONTRACT_ONLY
  future real ceiling LOCAL_SYNTHETIC_1000_VU_ONLY

PR #58 registry-signing contract
  head 1b543fdfad73377fa6ba51e3f190b56ed60452fa
  run  32266026763 PASS
  contract ceiling GITHUB_HOSTED_REGISTRY_SIGNING_RUNNER_CONTRACT_ONLY
  future real ceiling LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY
```

### PR #55 Argo rules

- Require one existing `kind-manager-demo-*` context.
- Refuse pre-existing `argocd` / `argo-rollouts` namespaces.
- Require exact HTTPS URL + SHA-256 for both install manifests.
- Hard-cap each manifest download at 20 MB.
- Apply with explicit runner-owned namespaces.
- Highest future receipt proves controllers + CRDs ready only, not Application reconciliation or live canary.

### PR #56 model rules

- Require exact llama.cpp commit, model HTTPS URL, model SHA-256 and admitted license ID.
- For selected Qwen demo lane, license ID is `Apache-2.0`; do not infer revision/file/SHA from the source registry.
- Build only `llama-cli`, build parallelism <=2, threads <=8, tokens <=128, timeout <=300s.
- Hard-cap model download at 2 GB and delete model/source/build bytes afterward.
- Highest future receipt is local inference only.

### PR #57 capacity rules

- Target loopback only and refuse an occupied port.
- Max 1,000 VU, spawn <=100/s, duration <=60s.
- Use temporary venv and no persistent pip cache.
- Require aggregate Locust stats, request count >0, p95 and failure-ratio gates.
- A future PASS remains synthetic capacity evidence only.

### PR #58 registry-signing rules

- Require exact registry image digest and exact cosign binary SHA-256.
- One loopback registry, one image build/push, one digest signature, ephemeral local keypair.
- No external registry credentials.
- Remove built local image, registry container and temporary key material.
- A future PASS is local registry signature evidence only; not production key custody/compliance.

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
CI_GREEN               → BUSINESS_CORRECT
RUNNER_CONTRACT_PASS   → PHYSICAL_RUNTIME_PASS
QUEUE_EXISTS           → QUEUE_EXECUTED
LOCAL_K8S_PASS         → PRODUCTION_INFRA_EXPERIENCE
ARGO_CONTROLLER_PASS   → APPLICATION_RECONCILIATION_PASS
LOCAL_MODEL_PASS       → PRODUCTION_LLM_TRAFFIC
1000_VU_PASS           → 1000_REAL_USERS
LOCAL_SIGNING_PASS     → PRODUCTION_KEY_CUSTODY
DRILL_COMPLETE         → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS  → BLANKET_LEGAL_CLEARANCE
CURRENT_PR_HEAD         → HISTORICAL_ARTIFACT_EVIDENCE
```

## Automation boundary

Unattended workers may create/update bounded code/docs/tests, run deterministic CI, emit candidate receipts and prepare draft PRs when contracts allow it. Stop on:

```text
stale/wrong subject
overlapping writer/resource lease
missing predecessor receipt
semantic conflict
required physical capability unavailable
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
issue closure when used as an authority transition
repository visibility / permission widening
production promotion / rollback admission
credential/provider enrollment
semantic conflict resolution
claims of real users, real incidents, production tenure or people-management tenure
```

## Next legal frontier

Do not activate M6 physical commands directly from GitHub contract CI. The legal order is:

```text
M5-LOCAL-REVIEWER-001 real PASS receipt
→ M5-LIVE-KIND-002 real PASS receipt
→ compile a new canonical Local Handoff epoch from exact PR #55/#56/#57/#58 runner subjects
→ execute only the newly admitted local commands
```

Until those receipts exist, physical M6 evidence remains `NOT_EXERCISED`.
