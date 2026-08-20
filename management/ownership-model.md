# Ownership Model

This document defines demo-system ownership roles. It is a portfolio artifact, not proof of historical people-management tenure.

## Bounded roles

| Role | Owns | May decide | Must escalate |
|---|---|---|---|
| Incident Commander | incident state, priorities, communication cadence | stop the bounded drill, order rollback/recovery, assign one executor per mutable surface | production/customer-impact decisions |
| Release Operator | release subject and rollback execution | execute the admitted non-production rollback/runbook | unknown rollback target, destructive migration |
| Service Owner | service SLI, dependency budgets, queue/backpressure | tune bounded demo limits and fail-fast behavior | production capacity changes |
| Observability Owner | detectors, SLI/SLO evidence | declare detector blind spot and require business signal | production alert routing |
| Security Owner | least-privilege/policy admission | reject missing/ambiguous authority | permission/visibility changes |
| Recovery Owner | backup/restore subject | execute deterministic restore drill and verify checksum | production data restore |
| Evidence Owner | receipts and evidence ceiling | reject evidence promotion without matching subject | real-experience/adoption claims |

## Ownership invariant

Exactly one role owns a mutable action at a time. Parallel work may share read-only evidence but may not share mutation authority without explicit Tech Lead reassignment.

## Escalation rule

Any production promotion/rollback, repository visibility/permission mutation, destructive data operation, real customer-impact statement, or employment/people-management claim is `HUMAN_ADMIT_REQUIRED`.
