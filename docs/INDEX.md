# Documentation & Traceability Index

Machine/evidence authority remains with exact registry subjects, executable checks, GitHub Actions artifacts, Local Handoff receipts, GitHub metadata and admitted runtime evidence. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_M7_ADVANCED_EXECUTION_BUNDLE_READY.md
→ registry/public-m7-advanced-bundle.json
→ registry/stack-plan.yaml
→ registry/mvp-demo-stack.yaml
→ handoff/local-handoff-queue.json
→ exact issue / PR / current head / evidence head / Actions run / artifact / runtime receipt
```

Historical milestones remain available in order:

```text
PUBLIC_REMOTE_FANOUT_FIRST_GREEN
→ PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN
→ PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN
→ PUBLIC_M5_LOCAL_KIND_RUNNER_READY
→ PUBLIC_M6_ADVANCED_RUNNER_CONTRACTS_READY
→ PUBLIC_M7_ADVANCED_EXECUTION_BUNDLE_READY
```

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | canonical Tech Lead / Shadow Architect / Git Town procedures |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe requirement/gap/prompt/narrative graph |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI, runtime/failure, Demo Console and Local Handoff receipts |
| Runtime contracts | `ed3c/runtime-env` when triggered | secret-free host/provider capability/workload contracts |
| External verification | `truth-verify-loop` / `openwiki-source-anchoring` when triggered | mutable/high-risk claim and exact source/path/quote verification |
| Human mirrors | Google Sheet / Google Doc | non-authoritative dashboard/narrative projections |

## Observed Full MVP route

```text
PR #6 bootstrap
└─ PR #12 Full MVP architecture
   └─ PR #13 evidence/invariant freeze
      └─ PR #14 Core
         ├─ PR #36 Observability
         ├─ PR #38 Policy/Security
         ├─ PR #39 ML/LLMOps
         ├─ PR #37 Demo Console
         └─ PR #40 Supply/Fault

PR #36
└─ PR #42 Failure/Recovery
     ↑ exact side evidence #38/#39/#40

PR #42
└─ PR #44 Reviewer Convergence
     ↑ exact Demo Console bytes #37 + M2/M3 artifacts
     └─ PR #45 historical Local Handoff bootstrap
          └─ PR #51 Live-kind Runner
               └─ PR #52 Canonical Local Handoff Queue
                    └─ PR #65 Advanced Execution Bundle
                         ↑ exact runner-byte side inputs #55/#56/#57/#58

M6 runner-contract task siblings:
PR #39 → PR #55 Argo
PR #39 → PR #56 Model
PR #36 → PR #57 Capacity
PR #40 → PR #58 Registry Signing
```

## Milestone status

```text
M1 CORE_REMOTE_FIRST_GREEN                          PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                 PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN       PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN   PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY          PASS_BOUNDED
M6 PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY            PASS_BOUNDED
M7 PUBLIC_ADVANCED_EXECUTION_BUNDLE_READY             PASS_BOUNDED
```

M7 is code/contract convergence, not physical execution.

## Canonical Local Handoff

Current method:

```text
ed3c/skills-shared@4ca9417b1da5ff32f1d4d3e7af64a15908749024
schema     agentic-tech-lead/local-handoff-queue/v1
assertion  skills/agentic-tech-lead-orchestration/scripts/assert_local_handoff_queue.py
```

Current canonical queue:

```text
PR #52 head      f7a3937d7d0979e3adfaf1ebc4adc0532450d925
execution commit 4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
execution tree   5ff3349c1eb5c7976263c2e89347a353ccbc1072
CI               32263239722 PASS
```

Physical queue frontier:

```text
M5-LOCAL-REVIEWER-001       ACTIVE / receipt ABSENT
        ↓ real PASS required
M5-LIVE-KIND-002            BLOCKED_BY_PREDECESSOR / receipt ABSENT
        ↓ real PASS required
M6-ADVANCED-SUBSTRATE-003   BLOCKED_BY_PREDECESSOR
```

No later runner/compiler may skip this chain.

## M6 current runner subjects

| PR | Lane | Current head | Actions run | Contract ceiling | Physical state |
|---:|---|---|---:|---|---|
| #55 | Argo + self-contained ephemeral kind owner | `8d976171…` | `32274548200` | `GITHUB_HOSTED_ARGO_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #56 | llama.cpp/model | `63355992…` | `32265971683` | `GITHUB_HOSTED_LOCAL_MODEL_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #57 | 1,000 VU | `2240e8ee…` | `32266078175` | `GITHUB_HOSTED_1000_VU_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #58 | registry signing | `1b543fdf…` | `32266026763` | `GITHUB_HOSTED_REGISTRY_SIGNING_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |

PR #55 old subject `284dbf1d…` remains historical evidence only. M7 found that the prior design assumed a live-kind cluster survived cleanup; the current PR #55 now creates and cleans its own scoped ephemeral kind cluster.

## M7 exact bundle subject

```text
Issue #60
PR    #65
head  cf63e2fc85d56c2e49cfefd33fefbec30316e1fa
tree  7dce94e01dd3630662deb6dfb3c67c8b5f272bb0
run   32275551599 PASS
```

Evidence ceiling:

```text
GITHUB_HOSTED_M7_ADVANCED_BUNDLE_AND_QUEUE_COMPILER_ONLY
```

PR #65 verifies exact imported runner byte parity, receipt-admission negative controls, explicit fixture/live separation, one-ACTIVE queue topology and the portable Local Handoff assertion/selftest. It performs no physical runtime.

## M7 future queue compiler

Live compilation requires both exact predecessor receipts from PR #52's execution epoch:

```text
reviewer PASS
  schema   full-manager-mvp/local-reviewer-handoff-receipt/v1
  ceiling  LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY

kind PASS
  schema   full-manager-mvp/local-kind-substrate-receipt/v1
  ceiling  LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

Fixtures are legal only with `--fixture-mode` and `evidence_kind=FIXTURE`. They can prove compiler behavior, never live completion.

Fixture-validated future order:

```text
M7-ARGO-CONTROLLERS-001       ACTIVE
→ M7-LOCAL-MODEL-002          BLOCKED_BY_PREDECESSOR
→ M7-CAPACITY-003             BLOCKED_BY_PREDECESSOR
→ M7-REGISTRY-SIGNING-004     BLOCKED_BY_PREDECESSOR
```

One ACTIVE item is intentional; physical resource ownership is serialized.

## Evidence closure route

```text
requirement
→ invariant / system contract
→ implementation
→ deterministic/runtime oracle
→ negative control / failure
→ detection + authority
→ mitigation / recovery
→ corrective change
→ same-failure re-test
→ exact receipt
→ reviewer packet
→ canonical Local Handoff at physical boundary
→ bounded evidence ceiling
```

Missing edges remain `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`. README/UI/issue/PR/queue/runner/compiler state cannot fill a missing physical receipt.

## Next physical boundary

```text
M5-LOCAL-REVIEWER-001 real PASS
→ M5-LIVE-KIND-002 real PASS
→ compile M7 canonical advanced queue in live mode
→ M7 Argo controllers
→ M7 local model
→ M7 synthetic 1,000 VU
→ M7 registry signing
```

A local or synthetic PASS is never production tenure, real user adoption, real incident history or people-management evidence.
