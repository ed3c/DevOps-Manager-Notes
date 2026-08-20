# Handoff Scripts

- `check_local_capabilities.py` — historical/base local capability reachability probe.
- `check_full_mvp_prerequisites.py` — Full Manager MVP prerequisite reachability probe; secret-free and non-mutating.
- `run_live_kind_smoke.py` — bounded Local Handoff runner for the first live kind/Kubernetes application-substrate proof.

## M5 live-kind runner

`run_live_kind_smoke.py` is intentionally split into two modes:

```text
--plan-only
  no Docker/kind/Kubernetes mutation
  validates cluster-name scope, exact kind-node digest, resource budget,
  cleanup contract and evidence ceiling

real execution
  requires local git + Docker daemon/buildx + kind + kubectl + python3
  creates exactly one new manager-demo-* kind cluster
  builds one OCI archive and binds its exact sha256 descriptor
  loads/deploys the app by digest
  exercises liveness/readiness plus business PASS and forced business FAIL
  records pod runtime image IDs and exact tool/runtime subjects
  deletes the created cluster and temporary files in finally
```

A real local PASS may prove only:

```text
LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

It does not prove Argo CD/Rollouts runtime, Qwen/llama.cpp, 1,000-VU behavior, production Kubernetes, production incidents/users, or people-management tenure.

The runner refuses arbitrary cluster names and refuses to take over an existing cluster. The kind node image must be supplied as an exact `name@sha256:<64 hex>` reference. It does not install tools or widen permissions.
