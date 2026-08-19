# DevOps Evidence & Traceability Index

This index routes humans and Agents to exact public evidence. It is navigation, not proof authority.

## Read route

```text
README.md
→ AGENTS.md
→ role contract
→ technology / Stack / evidence / gap registries
→ architecture contract
→ exact issue / PR / commit
→ implementation / test / failure artifact
→ durable receipt
```

## Core architecture

- `docs/architecture/DELIVERY_RELIABILITY_LAB.md` — implementation state machine, issue DAG, failure matrix, invariants and evidence lanes.
- `README.md` — directory→State Machine→DAG ownership, molecular Stack, technology URLs, local handoff and end-to-end data flow.

## Contracts and registries

- `roles/devops-manager/job-contract.yaml` — exact role requirements compiled from the source posting.
- `registry/evidence.yaml` — evidence ladder/state authority.
- `registry/gaps.yaml` — unresolved proof obligations.
- `registry/technology-candidates.yaml` — upstream repo/license/ADR admission inventory.
- `registry/stack-plan.yaml` — molecular task/branch/PR topology.

## Issue graph

```text
#1 requirement/invariant/evidence audit
 ↓
#2 base CI/CD → container → local Kubernetes delivery
 ├── #3 OTel / SLI-SLO / load
 └── #4 policy / security / dependency-license
       ↓ verified side inputs
#5 failure / rollback / incident / postmortem / re-test convergence
```

Start-readiness and completion-readiness are distinct; see README.

## Runtime handoff

- `scripts/handoff/check_local_capabilities.py` — bounded secret-free local capability probe.
- `handoff/local-handoff-queue.json` — typed zero-context continuation for genuine local-runtime evidence.
- `evidence/receipts/` — durable sanitized receipts created by admitted executions.

The queue is not a generic remote shell. Queue validity does not prove commands ran.

## Public evidence closure

```text
requirement
→ architecture/invariant
→ exact implementation subject
→ deterministic oracle
→ local/real substrate oracle where required
→ planted failure / negative control
→ mitigation/recovery
→ corrective change
→ same-failure re-test
→ evidence receipt + ceiling
```

Residual production, real-user adoption, real team-management tenure, provider credentials and Human promotion remain outside repository proof unless exact authorized evidence actually exists.
