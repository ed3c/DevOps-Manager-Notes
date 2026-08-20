# M5 — PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY

Status: `PASS_BOUNDED`

This milestone records that the first live kind/Kubernetes Local Handoff path has progressed from an unresolved placeholder into a **concrete, safety-reviewed runner and queue contract**. It does **not** record a local kind/Kubernetes execution.

## Exact runner subject

```text
Issue:          #47
PR:             #51
branch:         handoff/m5-live-kind-runner
base:           handoff/m4-local-runtime / PR #45
head:           20d2ccb0ed8c877309452eece7c755bb3411c4c1
tree:           7d4b5d5aaba2d023803b152ce5ac7f23f274eba0
contract run:   32259961112
run result:     SUCCESS
```

Contract evidence ceiling:

```text
GITHUB_HOSTED_LOCAL_RUNNER_CONTRACT_ONLY
```

Potential evidence ceiling **only after a real local PASS**:

```text
LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

## Runner behavior compiled

`run_live_kind_smoke.py` plus `run_live_kind_from_env.sh` now define a fixed Local Handoff contract:

```text
exact repo checkout
→ require git/python3/Docker daemon+buildx/kind/kubectl
→ require M5_KIND_NODE_IMAGE=name@sha256:<64 hex>
→ refuse arbitrary cluster name
→ refuse takeover of existing manager-demo-m5 cluster
→ build one OCI archive
→ bind exact OCI descriptor digest
→ create one manager-demo-* kind cluster
→ load exact archive
→ render deployment by immutable digest
→ apply bounded namespace/secret/deployment/service
→ wait for two ready replicas
→ record pod runtime image IDs
→ port-forward on bounded loopback port
→ infrastructure liveness/readiness probe
→ business PASS oracle
→ forced business FAIL oracle
→ receipt
→ terminate port-forward
→ delete attempted cluster
→ restore caller kubectl context
→ remove temporary files
```

The local SQLite secret contains demo-only non-credential state and is scoped to the temporary cluster.

## Resource / authority contract

```text
clusters created         <= 1
allowed name prefix      manager-demo-
expected cluster         manager-demo-m5
replicas                  2
pod CPU request           100m
pod CPU limit             1
pod memory request        128Mi
pod memory limit          512Mi
Local Handoff timeout     900 s
loopback port             18030
production operations     forbidden
permission widening       forbidden
```

The runner will not take ownership of a pre-existing cluster. A failed or partially completed `kind create` is treated as an attempted owned resource so cleanup still runs.

## Shadow Architect corrections

The first contract-green implementation triggered a second review.

### `LIFECYCLE / AUTHORITY_DELTA`

`kind create` changes the caller's current `kubectl` context. Treating cluster deletion as the only cleanup would leave host state changed.

Correction:

```text
capture current kubectl context
→ execute bounded kind work
→ restore prior context when one existed
```

### `FAILURE_SURFACE_DELTA`

An initial implementation marked the cluster as owned only after `kind create` returned successfully. A partial create could therefore leak resources.

Correction:

```text
cluster_attempted = true
before kind create
→ cleanup attempts kind delete even after partial failure
```

### `RESOURCE_DELTA`

The Local Handoff queue allows up to 900 seconds while an earlier plan description named 600 seconds. The hardened contract now distinguishes the 900-second outer handoff timeout from bounded individual operation timeouts.

### `EVIDENCE_DELTA`

An intermediate CI run failed because the workflow still asserted the pre-hardening cleanup text. The assertion was corrected and re-run; the failed run is not hidden or rewritten as evidence. Hardened contract run `32259961112` is the admitted runner-contract subject.

## Exact queue subject

```text
Issue:          #48
PR:             #52
branch:         handoff/m5-live-kind-queue
base:           handoff/m5-live-kind-runner / PR #51
head:           660d4deea81712f3d6ab5288ae09288b2e15cc27
queue run:      32260403160
run result:     SUCCESS
```

Queue validation evidence ceiling:

```text
GITHUB_HOSTED_LOCAL_HANDOFF_CONTRACT_VALIDATION_ONLY
```

## Queue state

The queue deliberately does not jump over the earlier local reviewer prerequisite:

```text
M4-LOCAL-REVIEWER-001
  state: ACTIVE
  command:
    bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
  receipt: ABSENT
        ↓ requires PASS_BOUNDED receipt

M4-LIVE-SUBSTRATE-002
  state: WAITING_PREDECESSOR
  runner: PR #51 @ 20d2ccb...
  required env:
    M5_KIND_NODE_IMAGE=name@sha256:<64 hex>
  command:
    bash scripts/handoff/run_live_kind_from_env.sh \
      --output evidence/local-kind/local-kind-receipt.json \
      --cluster-name manager-demo-m5 \
      --local-port 18030
        ↓ requires real local PASS receipt

M5-ARGO-MODEL-CAPACITY-003
  state: BLOCKED_UNRESOLVED
  commands: []
```

The advanced item remains commandless until exact Argo CD/Rollouts identities, Qwen/llama.cpp artifacts, resource budgets and abort/cleanup contracts exist.

## Required live-kind receipt

A future local execution must produce:

```text
evidence/local-kind/local-kind-receipt.json
schema: full-manager-mvp/local-kind-substrate-receipt/v1
verdict: PASS | FAIL
```

A PASS requires:

```text
local_kind_cluster_created               PASS
oci_digest_bound                         PASS
deployment_ready                         PASS
business_oracle_pass                     PASS
business_oracle_forced_fail_visible      PASS
pod_image_ids_captured                   PASS
cleanup                                  PASS
kubectl_context_restored                 PASS | SKIPPED_NO_PRIOR_CONTEXT
```

## Evidence boundary

This milestone does not prove:

```text
M4 local reviewer command executed             NOT_EXERCISED
local kind/Kubernetes application smoke        NOT_EXERCISED
real Argo CD reconciliation                    NOT_EXERCISED
live Argo Rollouts/Prometheus canary           NOT_EXERCISED
local Qwen/llama.cpp                           NOT_EXERCISED
1,000-VU capacity/recovery                     NOT_EXERCISED
registry-stored image signing                  NOT_EXERCISED
production Kubernetes/users/incidents          OUTSIDE_CURRENT_PROOF
people-management tenure                       OUTSIDE_REPOSITORY_PROOF
```

Illegal promotions:

```text
runner CI PASS       → local kind PASS                   forbidden
queue CI PASS        → local command executed            forbidden
local kind PASS      → production Kubernetes experience forbidden
local kind PASS      → Argo/model/1,000-VU PASS          forbidden
DRILL/local failure  → production incident history      forbidden
```

No L3 Shadow block remains for **runner + queue readiness**. The next proof frontier is a real Local Handoff receipt; current tooling cannot manufacture that receipt remotely.
