# Incident Drill Evidence Contract

This directory contains **public-safe drills and simulations**, not production incident history.

Every admitted incident exercise must bind an exact source/workflow subject and record this closed loop:

```text
trigger
→ detection
→ incident role / bounded authority
→ mitigation
→ recovery verification
→ postmortem
→ corrective change
→ same-failure re-test
→ exact receipt
```

## State machine

```text
PLANNED
→ TRIGGERED
→ DETECTED
→ INCIDENT_COMMAND_ACTIVE
→ MITIGATION_IN_PROGRESS
→ RECOVERED
→ POSTMORTEM_WRITTEN
→ CORRECTIVE_CHANGE_VERIFIED
→ SAME_FAILURE_RETESTED
→ CLOSED_AS_DRILL

missing evidence / failed recovery / failed re-test
→ OPEN_GAP
```

`CLOSED_AS_DRILL` must never be rewritten as `PRODUCTION_INCIDENT_RESOLVED`.

## Evidence states

Use only explicit states such as `PASS`, `FAIL`, `NOT_EXERCISED`, `NOT_IMPLEMENTED`, and `HUMAN_ADMIT_REQUIRED`. A green workflow is evidence only for the checks actually executed by that workflow.

## Public disclosure

Never publish secrets, customer identifiers, employer-confidential incident details, real access tokens, or private production topology. Real employment, people-management, customer impact, and production-incident claims require separate Human admission.
