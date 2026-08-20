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
→ registry/mvp-demo-stack.yaml
→ registry/stack-plan.yaml
→ registry/public-m2-first-green.json
→ registry/public-m3-failure-recovery.json
→ registry/public-m4-reviewer-convergence.json
→ registry/public-m5-local-kind-readiness.json
→ handoff/local-handoff-queue.json
→ exact issue / PR / commit / Actions run / artifact / runtime receipt
```

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow Architect / Git Town procedure |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe requirement/gap/prompt/narrative graph |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI, runtime/failure, Demo Console, Local Handoff receipts |
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
     └─ PR #45 M4 Local Handoff
          └─ PR #51 M5 Live-kind Runner
               └─ PR #52 M5 Queue Compiler
```

## Milestone status

```text
M1 CORE_REMOTE_FIRST_GREEN                         PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN                PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN      PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN  PASS_BOUNDED
M5 PUBLIC_LOCAL_KIND_RUNNER_AND_QUEUE_READY         PASS_BOUNDED
```

M5 means runner/queue readiness only. Local runtime is still unexecuted.

## M5 exact subjects

```text
Runner PR #51
  head 20d2ccb0ed8c877309452eece7c755bb3411c4c1
  tree 7d4b5d5aaba2d023803b152ce5ac7f23f274eba0
  CI   32259961112 PASS
  ceiling GITHUB_HOSTED_LOCAL_RUNNER_CONTRACT_ONLY

Queue PR #52
  head 660d4deea81712f3d6ab5288ae09288b2e15cc27
  CI   32260403160 PASS
  ceiling GITHUB_HOSTED_LOCAL_HANDOFF_CONTRACT_VALIDATION_ONLY
```

Queue frontier:

```text
M4-LOCAL-REVIEWER-001        ACTIVE / receipt ABSENT
        ↓ requires PASS_BOUNDED
M4-LIVE-SUBSTRATE-002        WAITING_PREDECESSOR / command concrete
        ↓ requires real local PASS
M5-ARGO-MODEL-CAPACITY-003   BLOCKED_UNRESOLVED / commands []
```

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
→ Local Handoff where physical substrate is required
→ bounded evidence ceiling
```

Missing edges remain `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`. README/UI/issue/queue state cannot fill a missing runtime receipt.

## Local Handoff

Canonical queue: `handoff/local-handoff-queue.json`.

Current ACTIVE command:

```bash
bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
```

Only after that receipt passes may the queue activate the concrete M5 live-kind command, which requires `M5_KIND_NODE_IMAGE` as an exact `name@sha256:<64 hex>` identity.

A future live-kind PASS is capped at `LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY`; it is not production Kubernetes experience and does not promote Argo/model/load states.
