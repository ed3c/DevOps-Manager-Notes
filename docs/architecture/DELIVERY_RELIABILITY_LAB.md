# Internal Platform Delivery & Reliability Lab

## Objective

Build a public, reproducible manager-level evidence loop for DevOps / Platform Engineering / SRE capability.

The lab proves only what the exact runtime and evidence receipts demonstrate. It does not claim production adoption, real team-management tenure, or production incident history.

## System flow

```text
source commit
→ CI tests
→ container build
→ security / dependency / license policy
→ immutable artifact identity
→ local Kubernetes deployment
→ readiness + business oracle
→ telemetry / SLI observation
→ controlled failure injection
→ incident decision
→ mitigation / rollback / recovery
→ postmortem
→ corrective change
→ same-failure re-test
→ evidence receipt
```

## State machine

```text
SOURCE_BOUND
→ BUILD_ADMITTED
→ ARTIFACT_VERIFIED
→ DEPLOYMENT_ADMITTED
→ RUNNING
→ OBSERVED
→ FAILURE_INJECTED
→ DEGRADED
→ MITIGATING
→ RECOVERED
→ POSTMORTEM_OPEN
→ CORRECTIVE_CHANGE_BOUND
→ REVERIFIED
→ CLOSED
```

Illegal promotions include:

```text
BUILD_GREEN → PRODUCTION_PROVEN
LOCAL_K8S_PASS → REAL_CLUSTER_PROVEN
LOAD_TEST_PASS → REAL_ADOPTION_PROVEN
DRILL_COMPLETE → PRODUCTION_INCIDENT_EXPERIENCE
SKIPPED_CHECK → PASS
```

## Issue DAG

### Start-readiness edges

```text
#1 contract/invariants
   ↓
#2 base delivery slice
   ├──► #3 observability/load
   ├──► #4 policy/security/license
   └──► #5 failure-drill design may begin after failure points are known
```

### Completion-readiness edges

```text
#1
→ #2
→ (#3 AND #4)
→ #5
```

#3 and #4 are path-disjoint after the base artifact/deployment contract is frozen and may execute in parallel. #5 may start earlier but cannot close until the failure, observability, and policy evidence it depends on is available.

## Candidate stack

Selection is provisional until ADRs close the relevant constraints:

```text
service            Python + FastAPI
container          Docker
local substrate    kind + Kubernetes
CI                 GitHub Actions
GitOps             Argo CD
telemetry          OpenTelemetry
metrics/SLO        Prometheus
load               Locust
policy             OPA
security/license   Trivy + explicit license policy
```

Optional ML/LLM-specific v2 lanes must not delay closure of the base reliability loop.

## Golden invariants

```text
INV-001 Artifact Identity
Every deployment names the exact source/artifact version it runs.

INV-002 Rollback Target
Every mutating deployment has a known previous good subject or an explicit no-rollback state before admission.

INV-003 Health != Business Correctness
Readiness alone cannot close the user-facing oracle.

INV-004 Bounded Resources
CPU, memory, queue depth, connections, retries and test duration are bounded or have a saturation oracle.

INV-005 Idempotent Recovery
Retry/reconciliation cannot duplicate irreversible side effects.

INV-006 Evidence Identity
PASS binds to subject, revision, workload, environment and evidence lane.

INV-007 Failure Observability
The system distinguishes failure, timeout, not attempted, skipped, partial success and unknown.

INV-008 Public Claim Ceiling
Public prose may not widen what the evidence proves.
```

## Failure matrix

At minimum exercise:

```text
bad application release
dependency timeout / slowdown
resource saturation
retry storm / duplicate request
credential or authorization failure
telemetry blind spot
rollback failure
backup/restore or DR assumption failure where practical
```

Each case must produce:

```text
trigger
→ detection
→ blast radius
→ incident authority
→ mitigation
→ recovery
→ root/causal analysis
→ corrective change
→ repeated probe
→ receipt
```

## Evidence lanes

```text
L0 source claim
L1 static reasoning
L2 deterministic test
L3 local integration
L4 real substrate
L5 adversarial / chaos
L6 production observation
```

The MVP is expected to close mainly L2-L3 and selected L4 semantics only where the runtime truly qualifies. Higher lanes remain explicit `NOT_EXERCISED` rather than inferred.
