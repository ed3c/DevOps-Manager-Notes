# Documentation & Traceability Index

Machine/evidence authority remains with exact registry subjects, executable checks, GitHub Actions artifacts, Local Handoff receipts, GitHub metadata and admitted runtime evidence. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md
→ docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md
→ docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md
→ docs/milestones/PUBLIC_M5_LOCAL_KIND_RUNNER_READY.md
→ docs/milestones/PUBLIC_M6_ADVANCED_RUNNER_CONTRACTS_READY.md
→ registry/mvp-demo-stack.yaml
→ registry/stack-plan.yaml
→ registry/public-m2-first-green.json
→ registry/public-m3-failure-recovery.json
→ registry/public-m4-reviewer-convergence.json
→ registry/public-m5-local-kind-readiness.json
→ registry/public-m6-runner-contracts.json
→ handoff/local-handoff-queue.json
→ exact issue / PR / current head / evidence head / Actions run / artifact / runtime receipt
```

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow Architect / Git Town procedures |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe requirement/gap/prompt/narrative graph |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI, runtime/failure, Demo Console and Local Handoff receipts |
| Runtime contracts | `ed3c/runtime-env` when triggered | secret-free host/provider capability/workload contracts |
| External verification | `truth-verify-loop` / `openwiki-source-anchoring` when triggered | fresh mutable claim/source verification |
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
     └─ PR #45 M4 Local Handoff bootstrap
          └─ PR #51 M5 Live-kind Runner
               └─ PR #52 Canonical Local Handoff Queue

M6 task-sibling contract leaves:
PR #39 → PR #55 Argo controller contract
PR #39 → PR #56 local model contract
PR #36 → PR #57 1,000-VU capacity contract
PR #40 → PR #58 registry-signing contract
```

## Milestone status

```text
M1 CORE_REMOTE_FIRST_GREEN                          PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                 PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN       PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN   PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY          PASS_BOUNDED
M6 PUBLIC_ADVANCED_RUNNER_CONTRACTS_READY            PASS_BOUNDED
```

M5/M6 mean runner/queue **contract readiness** only. Physical local runtime remains unexecuted.

## Canonical Local Handoff

A Shadow `CONTRACT_DRIFT` review found that the first M5 queue used consumer-only schema vocabulary. The corrected queue is PR #52 and is now gated by the portable `skills-shared` assertion.

```text
canonical method
  ed3c/skills-shared@4ca9417b1da5ff32f1d4d3e7af64a15908749024

PR #52 current head
  f7a3937d7d0979e3adfaf1ebc4adc0532450d925
  CI 32263239722 PASS

execution epoch
  commit 4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
  tree   5ff3349c1eb5c7976263c2e89347a353ccbc1072
```

Queue frontier:

```text
M5-LOCAL-REVIEWER-001       ACTIVE / receipt ABSENT
        ↓ requires real PASS receipt
M5-LIVE-KIND-002            BLOCKED_BY_PREDECESSOR / receipt ABSENT
        ↓ requires real PASS receipt
M6-ADVANCED-SUBSTRATE-003   BLOCKED_BY_PREDECESSOR
```

## M6 exact runner-contract subjects

| PR | Lane | Head | Actions run | Contract ceiling | Physical state |
|---:|---|---|---:|---|---|
| #55 | Argo controllers | `284dbf1d…` | `32265921102` | `GITHUB_HOSTED_ARGO_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #56 | llama.cpp/model | `63355992…` | `32265971683` | `GITHUB_HOSTED_LOCAL_MODEL_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #57 | 1,000 VU | `2240e8ee…` | `32266078175` | `GITHUB_HOSTED_1000_VU_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |
| #58 | registry signing | `1b543fdf…` | `32266026763` | `GITHUB_HOSTED_REGISTRY_SIGNING_RUNNER_CONTRACT_ONLY` | `NOT_EXERCISED` |

Exact trees, resource bounds, negative controls and potential real-PASS ceilings are in `registry/public-m6-runner-contracts.json`.

## Evidence closure route

```text
requirement
→ invariant / system contract
→ implementation
→ deterministic/runtime oracle
→ negative control / failure
→ detection + incident authority
→ mitigation / recovery
→ corrective change
→ same-failure re-test
→ exact receipt
→ reviewer packet
→ canonical Local Handoff when physical substrate is required
→ bounded evidence ceiling
```

Missing edges remain `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`. README/UI/issue/queue/runner state cannot fill a missing physical receipt.

## Next physical boundary

The legal execution order remains:

```text
M5-LOCAL-REVIEWER-001 real PASS
→ M5-LIVE-KIND-002 real PASS
→ compile next canonical queue epoch using exact PR #55/#56/#57/#58 runner subjects
→ execute Argo/model/1000-VU/signing commands only after that queue is admitted
```

A local PASS is never production tenure, real adoption, real incident history or people-management evidence.
