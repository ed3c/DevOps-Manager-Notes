# AGENTS.md

## Purpose

This public repository is the executable DevOps Manager / Platform Engineering / SRE evidence plane.

## Read order

1. `README.md`
2. `roles/devops-manager/job-contract.yaml`
3. `registry/evidence.yaml`
4. `registry/gaps.yaml`
5. nearest system-design, runbook, incident, test, or receipt artifact

## Operating mode

Default to `MONITOR`.

The Builder may explore reversible implementation choices. In parallel, Shadow Architect monitors material deltas in state, authority, ownership, lifecycle, concurrency, resources, external side effects, failure surface, and evidence.

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

L3 is reserved for unsafe/irreversible transitions, secret exposure, destructive migration without rollback, privilege expansion without authority, public claim inflation, or evidence promotion across unproven lanes.

## Tech Lead laws

- Freeze task scope, invariants, dependencies, acceptance criteria, budgets, and authority before fan-out.
- A dependency edge exists only when one task consumes another task's unmerged artifact/state.
- Parallel writers must have disjoint paths/resources.
- CI green, process exit zero, or worker self-report is not semantic correctness by itself.
- Every deployment side effect requires rollback/reconciliation semantics.
- Every retry path requires idempotency and bounded retry policy.
- Every resource that can grow requires an explicit bound or saturation oracle.
- Every SLO claim names workload, environment, percentile/window, and evidence lane.
- `FIRST_GREEN` triggers a failure-surface review.
- All synthetic incidents are labeled `DRILL` or `SIMULATION`.
- 1,000 virtual users never means 1,000 real users.
- Public evidence must be reproducible without any private repository dependency.

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

A lower lane never self-promotes into a higher lane.

## Closure rule

A manager capability is closed only through:

```text
requirement
→ architecture/invariant
→ implementation
→ observable SLI/SLO or correctness oracle
→ failure injection / negative control
→ incident decision + recovery
→ corrective change
→ repeated verification
→ durable evidence receipt
```

A successful deployment without a demonstrated failure/recovery path is incomplete manager evidence.

## Public/private boundary

Do not expose private repository URLs, credentials, customer/company identities, device identifiers, paid/private dependency inventory, or unverifiable business metrics. Repository visibility is a Human-owned boundary and must never be changed by an agent.
