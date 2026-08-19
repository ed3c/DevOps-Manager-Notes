# DevOps Manager Notes

Public, executable evidence repository for DevOps Manager / Platform Engineering / SRE management capability.

The repository is designed to prove a complete operational loop rather than collect disconnected notes. The central case is an internal AI/platform service that moves from source change to verified deployment, observability, failure injection, rollback, postmortem, and preventive re-verification.

## Scope

The repository owns public-safe evidence for:

- CI/CD and release engineering;
- Docker and Kubernetes platform operations;
- GitOps deployment and rollback;
- observability, SLI/SLO and error-budget design;
- capacity/load testing;
- security, policy and dependency/license gates;
- incident command, runbooks and postmortems;
- engineering-management ownership and operating models;
- failure drills that prove recovery rather than only first-green behavior.

No document may represent a drill as a production outage, virtual users as real adoption, or local evidence as production-scale proof.

## Canonical state machine

```text
PROBLEM_BOUND
→ SLO_DEFINED
→ DELIVERY_PATH_IMPLEMENTED
→ DEPLOYMENT_PROVED
→ OBSERVABILITY_PROVED
→ FAILURE_INJECTED
→ MITIGATION_PROVED
→ ROLLBACK_OR_RECOVERY_PROVED
→ POSTMORTEM_CLOSED
→ PREVENTIVE_CHANGE_VERIFIED

stale / mismatched evidence
→ GAP_REOPENED
```

## Target repository topology

```text
DevOps-Manager-Notes/
├── AGENTS.md
├── README.md
├── LICENSE
├── system-design/
│   ├── cicd-platform.md
│   ├── kubernetes-platform.md
│   ├── release-system.md
│   ├── observability.md
│   └── disaster-recovery.md
├── sre/
│   ├── sli-slo.md
│   ├── error-budget.md
│   ├── capacity-planning.md
│   └── availability-model.md
├── platform/
│   ├── app/
│   ├── docker/
│   ├── kubernetes/
│   ├── gitops/
│   └── policies/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── load/
│   └── failure/
├── observability/
│   ├── otel/
│   ├── prometheus/
│   ├── slo/
│   └── alerts/
├── incidents/
│   ├── drills/
│   └── postmortems/
├── runbooks/
├── management/
│   ├── ownership-model.md
│   ├── oncall-model.md
│   ├── delegation.md
│   └── delivery-metrics.md
├── evidence/
│   └── receipts/
└── .github/workflows/
```

Directories are created only with real artifacts. Presence of a path never means the capability is already proven.

## Reference MVP

The first public MVP is an **Internal Platform Delivery & Reliability Lab** with this vertical slice:

```text
commit
→ CI
→ build artifact
→ security/license policy
→ deploy to local Kubernetes
→ health + SLO observation
→ controlled failure injection
→ automated/manual mitigation
→ rollback/recovery
→ evidence receipt
→ postmortem
→ corrective change
→ repeated verification
```

Candidate implementation stack, subject to ADR admission:

```text
Python + FastAPI
Docker
kind / Kubernetes
GitHub Actions
Argo CD
OpenTelemetry
Prometheus
Locust
OPA
Trivy
```

Optional v2 lanes may add MLflow, Temporal, KServe, or vLLM only when the base operational loop is closed first.

## Evidence ladder

```text
L0 SOURCE_CLAIM
L1 STATIC_REASONING
L2 DETERMINISTIC_TEST
L3 LOCAL_INTEGRATION
L4 REAL_SUBSTRATE
L5 ADVERSARIAL / CHAOS
L6 PRODUCTION_OBSERVATION
```

Use exact evidence states:

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

Lower evidence never promotes itself into a higher lane.

## Shadow Architect monitor

Review material deltas in state, authority, ownership, lifecycle, concurrency, resources, external side effects, failure surface, and evidence. `FIRST_GREEN` triggers review; it does not close the work.

For every material delta:

1. What became newly possible?
2. What must now remain true?
3. How would we know it is false?

## Manager proof target

A strong artifact is not `deployment succeeded`.

The target loop is:

```text
failure
→ detection
→ incident decision
→ mitigation
→ recovery
→ postmortem
→ preventive change
→ same-failure re-test
→ PASS receipt
```

## First milestone

M0 is complete when the role contract, system-design backlog, failure matrix, public evidence policy, executable vertical-slice plan, and issue DAG are bound. M1 starts only after those contracts exist.
