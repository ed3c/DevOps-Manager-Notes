# Delegation and Execution Leases

This public artifact demonstrates a reproducible delegation model for the Manager MVP. It does not assert historical direct-report management experience.

## Delegation contract

Every delegated task binds:

```text
owner role
exact Git subject
objective / non-goals
allowed mutation paths
read-only inputs
start dependency
completion dependency
resource budget
stop condition
verification command
evidence ceiling
handoff target
```

## Lease rules

- Parallel workers require disjoint mutable paths or explicit serialization.
- Read-only evidence may be shared.
- A worker cannot widen its own authority or evidence ceiling.
- A failed verifier returns work to the same owner or an explicitly reassigned owner.
- Cross-lane convergence has one mutable owner and consumes other lanes as verified side inputs.

## Handoff completeness

A handoff is incomplete when it omits current state, last verified subject, residual blocker, or next executable action. Narrative summaries never substitute for an exact receipt.
