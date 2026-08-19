# AGENTS.md

## Purpose

This public repository is the executable DevOps Manager / Platform Engineering / SRE evidence plane for the Manager Evidence Graph.

`Product-Manager-Notes` owns private requirement/gap/orchestration/narrative state. This repository owns public-safe implementation, CI/runtime evidence, failure/recovery proofs, and receipts. Reusable procedure remains owned by `ed3c/skills-shared`.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `roles/devops-manager/job-contract.yaml`
4. `registry/evidence.yaml`
5. `registry/gaps.yaml`
6. `registry/technology-candidates.yaml`
7. `registry/stack-plan.yaml`
8. `docs/architecture/DELIVERY_RELIABILITY_LAB.md`
9. exact issue / PR / commit / Local Handoff subject
10. nearest system-design, runbook, incident, test, or receipt artifact

When procedure is required, read the canonical `skills-shared` implementations:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Use `runtime-env` only when a secret-free runtime/profile/workload contract is actually selected; do not make its declarations count as execution evidence.

## Operating mode

Default to `MONITOR`.

The Builder may explore reversible implementation choices. In parallel, Shadow Architect monitors material deltas in:

```text
ASSUMPTION
STATE
AUTHORITY
OWNERSHIP
LIFECYCLE
CONCURRENCY
RESOURCE
EXTERNAL_SIDE_EFFECT
FAILURE_SURFACE
EVIDENCE
```

For each material delta ask:

1. What became newly possible?
2. What must now remain true?
3. How would we know it is false?

Intervention levels:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

L3 is reserved for unsafe/irreversible transitions, secret exposure, destructive migration without rollback, privilege expansion without authority, uncontained failure injection, public claim inflation, or evidence promotion across unproven lanes.

## Tech Lead laws

- Freeze exact subject, scope, invariants, dependencies, acceptance criteria, budgets, authority, rollback and evidence lane before fan-out.
- Keep start-readiness and completion-readiness edges distinct.
- A Git true-child edge exists only when one branch consumes another branch's unmerged artifact/contract.
- Parallel writers require disjoint paths/resources; overlapping shared indexes have exactly one convergence owner.
- CI green, process exit zero, issue state, branch state, or Worker self-report is not semantic correctness by itself.
- Every deployment side effect requires rollback/reconciliation semantics.
- Every retry path requires idempotency and bounded retry policy.
- Every resource that can grow requires an explicit bound or saturation oracle.
- Every SLO/performance claim names workload, environment, percentile/window, duration and evidence lane.
- FIRST_GREEN triggers a failure-surface/evidence review and never closes work by itself.
- Synthetic incidents are `DRILL`/`SIMULATION`.
- 1,000 virtual users never means 1,000 real users.
- Local Kubernetes never means production-cluster experience.
- Public evidence must be reproducible without private repository dependency.

## Molecular Git Town laws

Follow `git-town-stacked-pr-worker`:

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract   → TRUE_CHILD
smallest behavior + tests + evidence      → TERMINAL_LEAF
shared final indexes / E2E                → CONVERGENCE
physical/runtime prerequisite             → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Atom vocabulary:

```text
C contract/schema/interface lock
K deterministic core
A adapter/provider/substrate
E eval/mutation/failure control
X convergence/E2E
D docs/receipt/handoff
```

Never invent a branch, PR, head SHA, merged state, or multi-parent ancestry. `registry/stack-plan.yaml` keeps nonexistent subjects `PLANNED` with null identities.

No Worker may autonomously resolve semantic conflicts, force push, ship, merge, release, promote, change visibility/permissions, or treat issue closure as runtime proof.

## Path/resource leases

Before a Worker writes, bind:

```text
allowed_paths
read_only_paths
forbidden_paths
runtime resources / ports / cluster names / artifact names
lease owner / attempt id
cleanup obligation
```

#3 observability/load and #4 policy/security are expected to be path-disjoint siblings after #2 freezes the base service/artifact interfaces. If either consumes the other's unmerged bytes, reclassify the actual relation rather than preserving a planned sibling fiction.

## Technology admission

`registry/technology-candidates.yaml` records the upstream repository and top-level license source. `VERIFIED_PERMISSIVE_TOP_LEVEL` is not a legal/compliance blanket clearance: transitive dependencies, base images, plugins, models and downloaded artifacts still require inventory and policy checks.

Technology is selected only after it maps to an admitted invariant/constraint and its operational burden, failure modes, lock-in, authority, migration and verification needs are recorded.

## Evidence states

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

Evidence ladder:

```text
L0 SOURCE_CLAIM
L1 STATIC_REASONING
L2 DETERMINISTIC_TEST
L3 LOCAL_INTEGRATION
L4 REAL_SUBSTRATE
L5 ADVERSARIAL_OR_CHAOS
L6 PRODUCTION_OBSERVATION
```

A lower lane never self-promotes into a higher lane. Receipt identity includes subject, revision, workload, environment and evidence lane.

## Closure rule

A manager capability is closed only through:

```text
requirement
→ architecture/invariant
→ implementation
→ observable business/SLI/SLO oracle
→ failure injection / negative control
→ incident decision + recovery
→ corrective change
→ repeated verification
→ durable exact-subject evidence receipt
```

A successful deployment without demonstrated failure/recovery is incomplete manager evidence.

## Local Handoff Execution Queue

Use `handoff/local-handoff-queue.json` only after remote work reaches a genuine local host/runtime/provider/forge boundary. Each item binds:

```text
entry exact commit/tree
→ required capabilities
→ concrete argv + cwd + timeout
→ sanitized durable receipt
→ required PASS exit
→ cleanup / next item
```

The queue must not contain secrets, machine credentials, private reasoning, or generic arbitrary shell commands. Queue shape validation is not execution evidence.

If a local receipt is absent or fails, keep downstream runtime claims blocked. A local executor may not infer merge, issue close, promotion, provider enrollment, permission changes, semantic conflict resolution, or production rollback.

## Public/private boundary

Do not expose private repository URLs, credentials, customer/company identities, device identifiers, paid/private dependency inventory, or unverifiable business metrics. Repository visibility is a Human-owned boundary.

Google Docs/Sheets are non-authoritative projections maintained by the Product control plane. Do not require them for public proof.

## Stop conditions

Stop or hand off on:

```text
stale/wrong subject
overlapping writer/resource lease
missing predecessor receipt
semantic conflict
required local capability unavailable
secret/private disclosure risk
unbounded retry/resource/failure injection
invalid or mismatched evidence receipt
failed cleanup
Human-owned transition
```
