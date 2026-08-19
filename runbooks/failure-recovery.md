# Failure / Recovery Runbook

Use this runbook only for bounded demo drills. Production actions remain Human-owned.

## Admission

Before triggering a drill, bind:

```text
source commit
fault profile
expected detector
rollback/recovery target
incident commander
executor role
stop condition
cleanup command or deterministic cleanup function
evidence ceiling
```

Do not start when the subject is stale, the rollback target is unknown, cleanup is unbounded, or another worker owns the same mutable surface.

## Execution loop

```text
OBSERVE baseline
→ TRIGGER one bounded fault
→ DETECT with the declared oracle
→ DECLARE incident role/authority
→ MITIGATE without widening authority
→ VERIFY recovery
→ WRITE postmortem
→ APPLY corrective change
→ RE-INJECT same failure
→ VERIFY detector/prevention still works
→ EMIT receipt
```

## Manager decision gates

- **Stop rollout:** business oracle or explicit SLO gate fails.
- **Rollback:** known previous-good subject exists and rollback is safer than continued diagnosis.
- **Fail closed:** authorization, artifact identity, policy, or evidence identity is ambiguous.
- **Escalate to Human:** production action, real customer impact, visibility/permission mutation, destructive data operation, or unclear ownership.

## Mandatory receipt fields

```text
scenario_id
classification = DRILL | SIMULATION
source_commit
trigger
detection
incident_authority
mitigation
recovery
postmortem
corrective_change
same_failure_retest
verdict
evidence_lane
evidence_ceiling
```

A failed same-failure re-test reopens the gap; it cannot be waived by prose.
