# On-call Model

This is a demo governance contract for the public Manager MVP, not evidence of a historical production on-call organization.

## State machine

```text
NORMAL
→ ALERTED
→ ACKNOWLEDGED
→ INCIDENT_COMMAND_ACTIVE
→ MITIGATING
→ RECOVERED
→ POSTMORTEM_PENDING
→ CORRECTIVE_ACTION_PENDING
→ REVERIFIED
→ CLOSED_AS_DRILL
```

## Response contract

- One Incident Commander owns incident priority and stop/rollback decisions.
- One executor owns each mutable surface.
- Handoffs must include current subject, observed state, active hypothesis, last safe action, rollback target, and next bounded action.
- A drill may be closed only after recovery verification and same-failure re-test.
- If the detector is unavailable or ambiguous, the state is `OPEN_GAP`, not PASS.

## Escalation boundaries

Escalate immediately for destructive operations, ambiguous authority, unavailable rollback, private-data exposure, or any production/customer-impact action. Those are outside automated portfolio execution.
