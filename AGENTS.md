# AGENTS.md

## Purpose

This repository is the public executable evidence plane for the Full Manager MVP Demo. Agents must preserve exact evidence subjects, bounded claims, true dependency graphs and public-safe content.

`Product-Manager-Notes` owns job requirements, product decisions, gap routing and interview narratives. `skills-shared` owns reusable Tech Lead, Shadow Architect, Git Town and Local Handoff procedures. This repository owns code, deterministic/runtime contracts, failure drills, reviewer evidence and typed local receipts.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_M8_MAIN_INTEGRATION.md`
5. `registry/public-m8-main-integration.json`
6. `registry/stack-plan.yaml`
7. `registry/evidence.yaml`
8. `registry/gaps.yaml`
9. `handoff/local-handoff-queue.json`
10. exact issue / PR / commit / workflow run / artifact / receipt
11. nearest directory README, contract and tests

Historical M2–M7 evidence is navigation input, not permission to raise an evidence ceiling.

Canonical Local Handoff method:

```text
repo      ed3c/skills-shared
commit    4ca9417b1da5ff32f1d4d3e7af64a15908749024
schema    agentic-tech-lead/local-handoff-queue/v1
assertion skills/agentic-tech-lead-orchestration/scripts/assert_local_handoff_queue.py
```

## Operating mode

Default: `MODE=MONITOR`.

Builder may perform reversible code/docs/tests, draft PRs and bounded remote CI. Shadow Architect independently watches:

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

Intervention:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

L3 includes secret/private disclosure, irreversible mutation without rollback, force push, permission widening, semantic conflict, overlapping resource ownership, unbounded load/download/fault/retry, failed cleanup, stale subject admission, fixture/live laundering, production claim inflation or merging with required checks red.

## Current admitted subjects

```text
main repository integration
  bb940bf7d5a3b1f605b79e9fb8f33c463a8ee5a7

M8 Local Handoff execution subject
  commit e7b4e23799a3579572598ebd5864a80831d49db4
  tree   0b72b9f09f73d3829db2f138d457a5691641bf79
  rollback bb940bf7d5a3b1f605b79e9fb8f33c463a8ee5a7

canonical method
  skills-shared@4ca9417b1da5ff32f1d4d3e7af64a15908749024
```

The execution subject and the mutable documentation PR head are different identities. Never replace one with the other.

## Evidence states and ladder

```text
PASS
PASS_BOUNDED
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
OUTSIDE_CURRENT_PROOF
OUTSIDE_REPOSITORY_PROOF
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

## Tech Lead laws

- Freeze exact subject, objective, non-goals, invariants, dependencies, resource budgets, rollback/cleanup, acceptance and evidence lane before fan-out.
- Start-readiness and completion-readiness are separate edges.
- A dependency exists only for real byte/state consumption or an admitted receipt.
- Git ancestry and task/process DAG are separate graphs.
- Parallel writers require disjoint path and runtime-resource leases.
- Every growing resource, external download, load or retry needs a hard bound.
- Every side effect requires cleanup, rollback or reconciliation.
- FIRST_GREEN triggers Shadow review; it does not close production proof.
- Issue/PR/branch/UI/worker status is candidate routing state, not capability evidence.
- Synthetic incidents remain `DRILL` or `SIMULATION`.
- A 1,000-VU run is not 1,000 users.
- Local Kubernetes is not production Kubernetes experience.
- Queue validation is not queue execution.

## Merge-after-green law

An Agent may prepare and, when explicitly authorized, merge a PR only when all are true:

```text
exact head is frozen
required workflows for that exact head are SUCCESS
scope matches the owning issue/task contract
PR is mergeable
no unresolved review thread or REQUEST_CHANGES exists
no semantic conflict is hidden by mechanical mergeability
rollback/evidence ceiling is recorded
no missing physical evidence is claimed as PASS
```

After a parent merge, child PRs must be retargeted or replaced by a clean integration leaf. Do not replay divergent ancestry when exact bytes are already in `main`; preserve the historical PR and use a clean convergence PR for missing files.

## Molecular Git Town laws

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical prerequisite                   → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Current integrated topology:

```text
#6 → #12 → #13 → #14
#14 → #36 → #42 → #44 → #45 → #51 → #52 → #65
#14 → #37 / #38 / #39 / #40
#39 → #55 / #56
#36 → #57
#40 → #58

#68 integrated the backbone
#37/#38/#39/#40 integrated path-disjoint capability lanes
#69 integrated exact #55–#58 contract tests/workflows
current M8 closure integrates docs/registry/queue
```

Historical PR #55–#58 were closed as integrated/superseded after exact bytes and tests reached `main`; they were not falsely marked as direct merges.

## Directory ownership

| Paths | Owner / rule |
|---|---|
| `platform/app/**` | Core behavior and business oracle; require tests and migration safety |
| `platform/kubernetes/**` | desired-state and live-kind contract; never imply production runtime |
| `platform/policies/**` | fail-closed policy/security metadata; never blanket legal clearance |
| `platform/rollouts/**`, `mlops/**` | lifecycle/eval/canary contract; live model/canary requires separate receipts |
| `observability/**`, `sre/**` | telemetry/SLO/load evidence with named workload and window |
| `supply-chain/**` | SBOM/signature/fault identities with cleanup and bounded artifacts |
| `tests/failure/**`, `incidents/**`, `runbooks/**` | drill closure; production history forbidden |
| `demo-console/**` | presentation only; cannot promote evidence |
| `scripts/handoff/**`, `handoff/**` | exact-subject local execution and receipt-gated queue |
| `registry/**` | machine routing, evidence identity and residual gaps |
| `docs/**`, `README.md`, `AGENTS.md` | navigation and bounded narrative only |

## Local Handoff law

Current queue: `handoff/local-handoff-queue.json`.

```text
M8-LOCAL-REVIEWER-001         ACTIVE
M8-LIVE-KIND-002              BLOCKED_BY_PREDECESSOR
M8-COMPILE-ADVANCED-QUEUE-003 BLOCKED_BY_PREDECESSOR
```

Every item binds execution subject `e7b4e23799a3579572598ebd5864a80831d49db4`.

Rules:

- Checkout the exact execution subject before running a command.
- Run only the current ACTIVE item.
- Persist the receipt at the declared path even on failure when the runner supports it.
- Do not advance based on terminal output or CI state; review the typed receipt.
- Queue advancement, semantic conflict resolution and provider activation remain Human/trusted-owner operations.
- After the compiler receipt passes, validate the generated advanced queue using the portable assertion and `--selftest` before activating its first item.
- Cleanup failure makes the owning receipt fail.

## Issue closure law

Close an issue only when its **declared stage scope** is complete and exact main reachability is recorded. Keep the issue open when the remaining requirement is a higher evidence lane.

Stage-complete issues may close after M8 merges:

```text
#1 evidence/invariant audit
#4 hosted policy/security/license gate
#5 deterministic failure/recovery drills
#8 Demo Console build
#10 hosted supply-chain/fault lane
#11 technology freeze
#16 repository visibility reconciliation
#22 public claim-inflation guard
#26 remote-only execution policy
#48 canonical queue/compiler contract
#54 advanced runner contracts
#60 M7 convergence/compiler
#61 M7 Shadow contract review
#62 M7 compiler validation
#63 M7 traceability
#64 fixture/negative-control validation
```

Keep open:

```text
#2 live kind/Kubernetes acceptance
#3 actual synthetic 1,000-VU run
#7 exact model artifact/local inference/live canary
#9 physical Local Handoff and advanced convergence
#67 repository-admin temporary-branch cleanup
```

Issue closure is not evidence promotion.

## Forbidden promotions

```text
CI_GREEN               → BUSINESS_CORRECT
RUNNER_CONTRACT_PASS   → PHYSICAL_RUNTIME_PASS
QUEUE_EXISTS           → QUEUE_EXECUTED
FIXTURE_PASS           → LIVE_RECEIPT_PASS
LOCAL_K8S_PASS         → PRODUCTION_INFRA_EXPERIENCE
ARGO_CONTROLLER_PASS   → APPLICATION_RECONCILIATION_PASS
LOCAL_MODEL_PASS       → PRODUCTION_LLM_TRAFFIC
1000_VU_PASS           → 1000_REAL_USERS
LOCAL_SIGNING_PASS     → PRODUCTION_KEY_CUSTODY
DRILL_COMPLETE         → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS  → BLANKET_LEGAL_CLEARANCE
REPO_ARTIFACT          → EMPLOYMENT_OR_MANAGER_TENURE
CURRENT_HEAD           → HISTORICAL_ARTIFACT_EVIDENCE
```

## Automation boundary

Unattended automation may create bounded code/docs/tests, run deterministic CI, emit candidate receipts and prepare draft PRs. Stop on:

```text
stale or wrong exact subject
missing predecessor receipt
merge conflict or semantic conflict
unbounded resource/fault/load/download/retry
secret/private material risk
permission or visibility change
provider/credential enrollment
failed cleanup
canonical method/schema drift
required physical capability unavailable
Human-owned transition
```

Human/trusted-owner operations:

```text
merge / force-push / release
queue advancement
repository visibility / permission changes
production promotion / rollback admission
provider or credential enrollment
semantic conflict resolution
claims of real users, real incidents, production tenure or people-management tenure
```
