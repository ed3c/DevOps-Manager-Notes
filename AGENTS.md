# AGENTS.md

## Purpose

This repository is the public executable evidence plane for the Full Manager MVP Demo. Agents must preserve exact evidence subjects, bounded claims, true Git/task dependencies, public-safe content and receipt-gated Local Handoff.

`Product-Manager-Notes` owns job requirements, product decisions, gap routing and interview narratives. `skills-shared` owns reusable Tech Lead, Shadow Architect, Git Town and Local Handoff procedures. This repository owns code, deterministic/runtime contracts, failure drills, reviewer evidence, typed local receipts and public-safe receipt projections.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_M9_LOCAL_RECEIPT_ADMISSION_READY.md`
5. `registry/public-m9-local-receipt-admission.json`
6. `registry/stack-plan.yaml`
7. `registry/evidence.yaml`
8. `registry/gaps.yaml`
9. `handoff/local-handoff-queue.json` before any physical/local continuation
10. exact issue / PR / commit / workflow run / artifact / raw receipt / admitted packet
11. nearest directory README, contract and tests

Historical M2–M8 evidence is navigation input, not permission to raise an evidence ceiling.

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

L3 includes secret/private disclosure, irreversible mutation without rollback, force push, permission widening, semantic conflict, overlapping resource ownership, unbounded load/download/fault/retry, failed cleanup, stale subject admission, fixture/live laundering, blocked-future receipt admission, queue/raw-receipt overwrite, production claim inflation or merging with required checks red.

## Current checkpoints

```text
M1 CORE_REMOTE_FIRST_GREEN                          PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                 PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN       PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN   PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY          PASS_BOUNDED
M6 PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY            PASS_BOUNDED
M7 PUBLIC_ADVANCED_EXECUTION_BUNDLE_READY             PASS_BOUNDED
M8 PUBLIC_MAIN_INTEGRATION_AND_HANDOFF_READY           PASS_BOUNDED
M9 PUBLIC_LOCAL_RECEIPT_ADMISSION_READY                PASS_BOUNDED
```

M9 proves an admission/projection contract only. It does not prove any physical Local Handoff command executed.

## Current admitted M9 subject

```text
A9 PR #77
head    fc7ae40c0a5ea0a403c2ed27555de3cbbc8d042b
tree    67acc95ed6ee85091dfe30c8b853bc54203c3cda
run     32376416583 PASS
ceiling GITHUB_HOSTED_M9_RECEIPT_ADMISSION_CONTRACT_ONLY
```

The exact head may move only through the planned D9 traceability integration; after any move, re-run exact-head CI and do not relabel the older run as new-head evidence.

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
- Queue validation and public packet compilation are not queue execution.

## Exact subject law

Keep these identities separate:

```text
current_head     mutable PR routing identity
evidence_head    exact commit that produced an admitted CI/artifact
queue_subject    exact commit/tree every local receipt must match
compiler_subject exact commit/tree of the admission code itself
```

Never use a current PR head to rewrite the subject of historical evidence. Never accept a raw receipt whose repository/commit/tree differs from the queue subject.

## Merge-after-green law

A PR may be merged only when all are true:

```text
exact head is frozen
required workflows for that exact head are SUCCESS
scope matches owning issue/task contract
PR is mergeable
no unresolved REQUEST_CHANGES or semantic conflict exists
rollback/evidence ceiling is recorded
no missing physical evidence is claimed as PASS
```

After a true-child D9 traceability PR is merged into A9, A9's head changes. Re-run A9 required CI on the resulting exact head before merging A9 to `main`.

## Molecular Git Town laws

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical prerequisite                   → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Current M9 shape:

```text
main
└─ A9 PR #77 local receipt admission
   └─ D9 M9 traceability child
```

D9 consumes A9's unmerged admission contract and is therefore a TRUE_CHILD. Physical Local Handoff receipts are process dependencies, not Git parents.

## Directory ownership

| Paths | Owner / rule |
|---|---|
| `platform/app/**` | Core behavior/business oracle; require tests and migration safety |
| `platform/kubernetes/**` | desired-state/live-kind contract; never imply production runtime |
| `platform/policies/**` | fail-closed policy/security metadata; never blanket legal clearance |
| `platform/rollouts/**`, `mlops/**` | lifecycle/eval/canary contract; live model/canary requires separate receipts |
| `observability/**`, `sre/**` | telemetry/SLO/load evidence with named workload/window |
| `supply-chain/**` | SBOM/signature/fault identities with cleanup/bounded artifacts |
| `tests/failure/**`, `incidents/**`, `runbooks/**` | drill closure; production history forbidden |
| `demo-console/**` | presentation only; cannot promote evidence |
| `scripts/handoff/run_*` | physical command runners and raw typed receipts |
| `scripts/handoff/compile_m7_advanced_queue.py` | candidate advanced queue compiler; never executes advanced runtime |
| `scripts/handoff/compile_public_receipt_packet.py` | M9 parsing/projection core; do not call directly for live public admission |
| `scripts/handoff/admit_public_receipt_packet.py` | **authoritative M9 admission CLI** |
| `handoff/**` | exact-subject queue; trusted advancement only |
| `evidence/local-handoff/**` | public-safe admitted packet output; projection only |
| `registry/**` | machine routing/evidence identity/residual gaps |
| `docs/**`, `README.md`, `AGENTS.md` | navigation and bounded narrative only |

## Local Handoff law

Current canonical queue: `handoff/local-handoff-queue.json`.

```text
execution subject
  commit e7b4e23799a3579572598ebd5864a80831d49db4
  tree   0b72b9f09f73d3829db2f138d457a5691641bf79

M8-LOCAL-REVIEWER-001         ACTIVE
M8-LIVE-KIND-002              BLOCKED_BY_PREDECESSOR
M8-COMPILE-ADVANCED-QUEUE-003 BLOCKED_BY_PREDECESSOR
```

Rules:

- Checkout the exact execution subject before running a command.
- Run only the current ACTIVE item.
- Persist the typed raw receipt at the declared path.
- Do not advance from terminal output, CI state or packet existence.
- Cleanup failure makes the owning receipt fail.
- Queue advancement, semantic-conflict resolution and provider activation remain Human/trusted-owner operations.
- After the compile receipt passes, validate the generated advanced queue using the portable assertion and `--selftest` before activation.

## M9 public receipt admission law

For public evidence, the only supported entrypoint is:

```text
scripts/handoff/admit_public_receipt_packet.py
```

The wrapper enforces:

```text
queue state: COMPLETE* → ACTIVE → BLOCKED_BY_PREDECESSOR*
exact queue subject
receipt contiguous prefix ending at or before current ACTIVE
no blocked-future receipt admission
no FAIL receipt for already COMPLETE items
exact receipt schema/repository/commit/tree/verdict/ceiling/cleanup
explicit bounded receipt roots; filesystem root forbidden
fixture/live isolation
secret-like and sensitive-key rejection
allowlisted summaries only
live output only under evidence/local-handoff
output cannot overwrite queue or raw receipt
queue_mutated=false
queue_advanced=false
```

The lower-level `compile_public_receipt_packet.py` remains testable core logic, but it does not own the live public authority boundary.

After a raw current-ACTIVE receipt exists, a typical projection is:

```bash
python3 scripts/handoff/admit_public_receipt_packet.py \
  --queue handoff/local-handoff-queue.json \
  --receipt-root evidence/local-reviewer \
  --receipt M8-LOCAL-REVIEWER-001=handoff-receipt.json \
  --output evidence/local-handoff/public-receipt-packet.json
```

Possible aggregate routing states:

```text
LOCAL_GAP_OPEN
ACTIVE_RECEIPT_REQUIRED
HUMAN_QUEUE_ADVANCE_REQUIRED
QUEUE_COMPLETION_REVIEW_REQUIRED
```

None is an unattended queue transition.

## Issue closure law

Close an issue only when its **declared stage scope** is complete and exact `main` reachability is recorded. Keep an issue open when the remaining requirement belongs to a higher evidence lane.

Current open residuals after M8 plus M9 work:

```text
#2   live kind/Kubernetes acceptance
#3   actual synthetic 1,000-VU run
#7   exact model artifact/local inference/live canary
#9   physical Local Handoff and advanced convergence
#67  repository-admin temporary-branch cleanup
#76  M9 receipt admission until merged to main
#78  M9 traceability child until merged to main
```

Issue closure is not evidence promotion.

## Forbidden promotions

```text
CI_GREEN                → BUSINESS_CORRECT
RUNNER_CONTRACT_PASS    → PHYSICAL_RUNTIME_PASS
QUEUE_EXISTS            → QUEUE_EXECUTED
FIXTURE_PASS            → LIVE_RECEIPT_PASS
RECEIPT_PACKET_EXISTS   → RAW_RUNTIME_REEXECUTED
PUBLIC_PACKET_PASS      → QUEUE_ADVANCED
BLOCKED_RECEIPT_EXISTS  → BLOCKED_ITEM_COMPLETE
LOCAL_K8S_PASS          → PRODUCTION_INFRA_EXPERIENCE
ARGO_CONTROLLER_PASS    → APPLICATION_RECONCILIATION_PASS
LOCAL_MODEL_PASS        → PRODUCTION_LLM_TRAFFIC
1000_VU_PASS            → 1000_REAL_USERS
LOCAL_SIGNING_PASS      → PRODUCTION_KEY_CUSTODY
DRILL_COMPLETE          → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS   → BLANKET_LEGAL_CLEARANCE
REPO_ARTIFACT           → EMPLOYMENT_OR_MANAGER_TENURE
CURRENT_HEAD            → HISTORICAL_ARTIFACT_EVIDENCE
```

## Automation boundary

Unattended automation may create bounded code/docs/tests, run deterministic CI, emit candidate receipts and prepare draft PRs. Stop on:

```text
stale or wrong exact subject
missing predecessor receipt
receipt for a BLOCKED future item
merge conflict or semantic conflict
unbounded resource/fault/load/download/retry
secret/private material risk
queue/raw-receipt overwrite risk
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
