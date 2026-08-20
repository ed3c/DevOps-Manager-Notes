# M8 — PUBLIC_MAIN_INTEGRATION_AND_HANDOFF_READY

Status: `PASS_BOUNDED`

M8 reconciles the public molecular Stack into `main`, preserves exact historical evidence, adds missing advanced-runner contract tests/workflows through a clean convergence leaf, and creates a new exact-subject Local Handoff queue. It does not execute physical local or production runtime lanes.

## Main integration sequence

| Order | PR | Purpose | Merge commit |
|---:|---:|---|---|
| 1 | #68 | M1–M7 backbone: Core, observability, failure/recovery, reviewer, canonical queue, live-kind contract, M7 compiler | `d0ecbd05c1dfecc6ae65f62c9869cd6a1412da43` |
| 2 | #37 | Manager Demo Console | `a47c0de9d5d0a176821a95c7a6c961ed7cf9f058` |
| 3 | #38 | Policy/security/license metadata gates | `cf7f0f5939e75475ce10da14f932de1a7f33b257` |
| 4 | #39 | MLflow lifecycle/eval/rollback/progressive-delivery contract | `9e5b9c23467ff90a1c1452a255d4a6cfa245b6bf` |
| 5 | #40 | SBOM/same-run signing/bounded fault | `0b0709946e84e80918a0e50903badb8b7bd4fa12` |
| 6 | #69 | exact advanced runner contract workflows/tests | `bb940bf7d5a3b1f605b79e9fb8f33c463a8ee5a7` |

PR #68 exact-head main-base workflows were all green before merge: Core, observability/load, failure/recovery, reviewer convergence, public artifact convergence, canonical Local Handoff, live-kind runner contract and M7 bundle/compiler.

PR #69 exact-head contract runs were all green:

```text
Argo runner contract       32325970179 SUCCESS
Model runner contract      32325970269 SUCCESS
Capacity runner contract   32325970231 SUCCESS
Registry-signing contract  32325970178 SUCCESS
```

## Divergent-ancestry correction

After #68 merged, historical runner PR #55–#58 attempted to re-add exact runner paths that were already in `main` through M7 convergence. Direct replay merges would have obscured ownership and created add/add conflicts.

Corrective route:

```text
exact runner bytes #55/#56/#57/#58
  → already in #68 main backbone
missing exact tests/workflows
  → clean PR #69 from current main
historical PRs
  → close as integrated/superseded with exact comments
```

No implementation was rewritten. PR #69 used the existing source blobs from the exact historical heads.

## M8 Local Handoff execution subject

A two-phase closure creates a stable execution subject before writing the queue that references it:

```text
commit   e7b4e23799a3579572598ebd5864a80831d49db4
tree     0b72b9f09f73d3829db2f138d457a5691641bf79
rollback bb940bf7d5a3b1f605b79e9fb8f33c463a8ee5a7
```

This subject contains all local runners plus `compile_m8_advanced_queue.py`, which delegates to the M7 compiler while requiring an explicitly admitted predecessor commit/tree.

## Queue

Canonical file: `handoff/local-handoff-queue.json`.

```text
M8-LOCAL-REVIEWER-001             ACTIVE
  ↓ exact PASS receipt
M8-LIVE-KIND-002                  BLOCKED_BY_PREDECESSOR
  ↓ exact PASS receipt + cleanup
M8-COMPILE-ADVANCED-QUEUE-003     BLOCKED_BY_PREDECESSOR
  ↓ compile receipt + portable assertion/selftest + Human review
M7 advanced runtime queue         NOT_COMPILED
```

The compiler command binds both predecessor receipts to the same M8 execution subject. Fixture receipts remain forbidden in live mode.

## Issue/PR reconciliation

### Stage-complete after this closure merges

```text
issues: #1 #4 #5 #8 #10 #11 #16 #22 #26 #48 #54 #60 #61 #62 #63 #64
```

These close only at their declared contract/stage evidence ceilings.

### Remain open

```text
#2  live kind/Kubernetes application acceptance
#3  real synthetic 1,000-VU execution
#7  exact model artifact/local inference/live canary
#9  physical Local Handoff and advanced convergence
#67 temporary branch deletion by repository admin
```

### Historical PR handling

```text
#55–#58 closed as integrated/superseded via #68/#69
#15 closed as superseded by canonical #52
ancestor implementation PRs closed after main reachability is recorded
historical docs PRs closed after M8 copies their exact milestones/registries
```

## Shadow Architect verdict

```text
STATE_DELTA               main now contains verified public implementation surfaces
LIFECYCLE_DELTA           Argo owns an ephemeral cluster; no disposed-cluster dependency
AUTHORITY_DELTA           merge and queue advancement remain explicit admissions
OWNERSHIP_DELTA           clean integration owners replace divergent replay merges
CONCURRENCY_DELTA         advanced local queue remains sequential
RESOURCE_DELTA            runner bounds and cleanup contracts preserved
FAILURE_SURFACE_DELTA     negative controls remain executable
EVIDENCE_DELTA            main reachability, historical evidence and local runtime stay distinct
CONTRACT_DRIFT             canonical skills-shared queue schema/assertion retained
```

No L3 blocker remains for M8 repository-integration and Local-Handoff readiness.

## Evidence ceiling

```text
GITHUB_MAIN_INTEGRATION_AND_LOCAL_HANDOFF_CONTRACT_ONLY
```

Not exercised:

```text
local deterministic reviewer
live kind/Kubernetes
Argo controllers/Application reconciliation/Rollouts canary
llama.cpp/model inference
synthetic 1,000-VU run
registry-stored signing
production users/incidents/tenure
people-management tenure
```

No repository artifact can manufacture employment history, production operation history, real adoption or people-management experience.
