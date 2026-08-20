# M6 — PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY

Status: `PASS_BOUNDED`

This milestone records two things:

1. the M5 Local Handoff queue was recompiled against the **current canonical Tech Lead method** after Shadow Architect detected consumer/schema drift; and
2. four remaining advanced local-substrate obligations now have concrete, bounded runner contracts with GitHub-hosted no-side-effect FIRST_GREEN evidence.

It does **not** record any physical/local execution of those runners.

## Canonical Local Handoff correction

The previous consumer queue used custom states/fields and a custom validator. A later canonical-method readback treated that as `CONTRACT_DRIFT`; issue #48 was reopened and PR #52 was hardened instead of hiding the mismatch.

Canonical method subject:

```text
repo    ed3c/skills-shared
commit  4ca9417b1da5ff32f1d4d3e7af64a15908749024
schema  agentic-tech-lead/local-handoff-queue/v1
assert  skills/agentic-tech-lead-orchestration/scripts/assert_local_handoff_queue.py
```

Canonical queue PR:

```text
PR      #52
head    f7a3937d7d0979e3adfaf1ebc4adc0532450d925
tree    ff9febf611b4a88d424e0ee95e4667eba6a11bf3
run     32263239722
result  SUCCESS
```

The execution epoch bound by the queue is:

```text
commit   4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
tree     5ff3349c1eb5c7976263c2e89347a353ccbc1072
rollback 660d4deea81712f3d6ab5288ae09288b2e15cc27
```

Portable assertion, negative-control selftest and exact execution-subject readback passed. Evidence ceiling remains:

```text
GITHUB_HOSTED_CANONICAL_LOCAL_HANDOFF_CONTRACT_ONLY
```

No local command was executed by that workflow.

## M6 molecular runner-contract fan-out

```text
PR #39 ML/LLMOps
├─ A6 PR #55 Argo control-plane contract
└─ A6 PR #56 llama.cpp/model contract

PR #36 Observability/Load
└─ E6 PR #57 1,000-VU capacity contract

PR #40 Supply/Fault
└─ E6 PR #58 local registry-signing contract
```

These are task siblings. Their Git parents differ because each consumes a different unmerged implementation lane. No fake common Git parent or multi-parent convergence is created.

## Exact current contract subjects

| PR | Lane | Head | Tree | Actions run | Contract ceiling | Potential ceiling after real local PASS |
|---:|---|---|---|---:|---|---|
| #55 | Argo CD / Rollouts controllers + self-contained ephemeral kind owner | `8d976171f4aa2eba72bee360823b660f9bed99d4` | `fada58f36c83de296decb41dcd34531b9d73145a` | `32274548200` | `GITHUB_HOSTED_ARGO_RUNNER_CONTRACT_ONLY` | `LOCAL_ARGO_CONTROLLERS_READY_ONLY` |
| #56 | llama.cpp + exact model artifact | `63355992f382cf260c624e2c7c7c3733cce82c20` | `973f91c0354d43a679c558394ef9f2a6da58ac9a` | `32265971683` | `GITHUB_HOSTED_LOCAL_MODEL_RUNNER_CONTRACT_ONLY` | `LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY` |
| #57 | synthetic 1,000 VU | `2240e8ee7ae9f151503d5c03d8043938dbbdce95` | `7965e4c544715d601de455d0839a9576649d8f73` | `32266078175` | `GITHUB_HOSTED_1000_VU_RUNNER_CONTRACT_ONLY` | `LOCAL_SYNTHETIC_1000_VU_ONLY` |
| #58 | loopback registry image signing | `1b543fdfad73377fa6ba51e3f190b56ed60452fa` | `266d81dbb51b0d2422deafdb829b2ef8f1f163ff` | `32266026763` | `GITHUB_HOSTED_REGISTRY_SIGNING_RUNNER_CONTRACT_ONLY` | `LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY` |

All four current contract workflows passed. They compile/test plan and negative-control contracts only; they do not perform physical runtime operations.

The earlier PR #55 evidence subject `284dbf1d...` / run `32265921102` remains historical contract evidence only. It is not relabeled as evidence for the hardened PR #55 current head.

## Shadow Architect hardening ledger

### Local Handoff `CONTRACT_DRIFT`

The consumer queue initially diverged from the portable `skills-shared` schema. Corrective action:

```text
custom states/classes/fields + custom validator
→ canonical state/class/authority vocabulary
→ one shared execution-subject epoch
→ canonical PASS exit receipts
→ portable assertion + selftest
```

### Argo `LIFECYCLE / AUTHORITY / RESOURCE / EVIDENCE_DELTA`

Initial M6 hardening already required:

- explicit runner-owned `argocd` and `argo-rollouts` namespaces;
- namespace takeover refusal;
- explicit namespace apply/delete;
- two manifest downloads, each capped at 20 MB and SHA-256 verified.

A later M7 dependency review found a real lifecycle mismatch: the M5 live-kind runner correctly deletes its cluster during cleanup, so a later advanced Argo item could not legally assume that cluster still existed. PR #55 was hardened again rather than preserving the false dependency.

The current self-contained Argo lane now:

```text
exact kind node image digest
→ refuse pre-existing manager-demo-* cluster
→ capture caller kubectl context
→ create one bounded ephemeral kind cluster
→ run exact Argo controller install contract
→ require inner controller + cleanup PASS
→ delete attempted cluster
→ restore caller kubectl context
```

Highest possible future receipt remains controller readiness only. It cannot claim Argo CD Application reconciliation, live Rollouts canary analysis, production Kubernetes, production deployment or customer traffic.

### Model `RESOURCE / EVIDENCE_DELTA`

- exact llama.cpp commit, model URL, SHA-256 and `Apache-2.0` license identifier are required at execution;
- model download is hard-capped at 2 GB with Content-Length and streaming byte checks;
- build parallelism <=2, inference threads <=8, output tokens <=128, timeout <=300 seconds;
- model/source/build bytes are temporary and deleted;
- current Qwen descriptor remains `NOT_EXERCISED` until exact artifact identity is supplied.

### Capacity `AUTHORITY / RESOURCE / EVIDENCE_DELTA`

- loopback-only target and occupied-port refusal;
- max 1,000 VU, spawn <=100/s, duration <=60s;
- temporary venv with no persistent pip cache;
- explicit p95/failure-ratio gates and aggregate-stat requirement;
- a future 1,000-VU PASS remains synthetic load evidence, never 1,000 real users.

### Registry signing `AUTHORITY / RESOURCE / EVIDENCE_DELTA`

- exact registry image digest and cosign binary SHA-256 required;
- one loopback registry, one image push, one signature, ephemeral local keypair only;
- no external registry credentials;
- digest-addressed sign/verify with local HTTP registry explicitly opted in;
- built local image tag, registry container and key/temp material are cleanup-owned;
- a future PASS does not prove production key custody or organization-wide compliance.

## State Machine frontier

```text
M4_REMOTE_REVIEWER_PASS
→ M5_CANONICAL_QUEUE_READY
→ M5_LOCAL_REVIEWER_ACTIVE                    receipt ABSENT
→ M5_LIVE_KIND_BLOCKED_BY_PREDECESSOR         receipt ABSENT
→ M6_ADVANCED_RUNNER_CONTRACTS_READY          this milestone
→ M7 advanced bundle/compiler                 contract work may start
→ future canonical advanced queue epoch       requires predecessor receipts
→ Argo/model/1000-VU/signing physical receipts NOT_EXERCISED
```

Runner-contract readiness does not skip the active Local Handoff predecessor chain.

## Residual evidence boundary

```text
local deterministic reviewer execution       NOT_EXERCISED
local kind/Kubernetes application smoke       NOT_EXERCISED
Argo CD/Rollouts controller runtime           NOT_EXERCISED
Argo CD Application reconciliation            NOT_EXERCISED
live Rollouts/Prometheus canary                NOT_EXERCISED
llama.cpp/model inference                     NOT_EXERCISED
1,000-VU synthetic capacity                   NOT_EXERCISED
registry-stored image signature               NOT_EXERCISED
production Kubernetes/users/incidents         OUTSIDE_CURRENT_PROOF
production LLM traffic / deployment tenure    OUTSIDE_CURRENT_PROOF
people-management tenure                      OUTSIDE_REPOSITORY_PROOF
```

No L3 Shadow blocker remains for **M6 runner-contract readiness**. Physical execution remains Local Handoff work, and merge/release/visibility/production/real-experience admission remains Human-owned.
