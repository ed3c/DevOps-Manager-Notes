# Documentation & Traceability Index

Machine/evidence authority remains with exact Git subjects, executable checks, Actions artifacts and admitted Local Handoff receipts. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_M8_MAIN_INTEGRATION.md
→ registry/public-m8-main-integration.json
→ registry/stack-plan.yaml
→ handoff/local-handoff-queue.json
```

## Milestone route

| Milestone | Narrative | Machine index | State |
|---|---|---|---|
| M1 Core | Core PR #14 and Actions evidence | `registry/evidence.yaml` | `PASS_BOUNDED` |
| M2 Fan-out | `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md` | `registry/public-m2-first-green.json` | `PASS_BOUNDED` |
| M3 Failure/recovery | `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md` | `registry/public-m3-failure-recovery.json` | `PASS_BOUNDED` |
| M4 Reviewer convergence | `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md` | `registry/public-m4-reviewer-convergence.json` | `PASS_BOUNDED` |
| M5 Local runner/queue readiness | `docs/milestones/PUBLIC_M5_LOCAL_KIND_RUNNER_READY.md` | `registry/public-m5-local-kind-readiness.json` | `PASS_BOUNDED` |
| M6 Advanced runner contracts | `docs/milestones/PUBLIC_M6_ADVANCED_RUNNER_CONTRACTS_READY.md` | `registry/public-m6-runner-contracts.json` | `PASS_BOUNDED` |
| M7 Advanced bundle/compiler | `docs/milestones/PUBLIC_M7_ADVANCED_EXECUTION_BUNDLE_READY.md` | `registry/public-m7-advanced-bundle.json` | `PASS_BOUNDED` |
| M8 Main integration/handoff | `docs/milestones/PUBLIC_M8_MAIN_INTEGRATION.md` | `registry/public-m8-main-integration.json` | `PASS_BOUNDED` |

## Integrated main chain

```text
PR #68 → d0ecbd05c1dfecc6ae65f62c9869cd6a1412da43
PR #37 → a47c0de9d5d0a176821a95c7a6c961ed7cf9f058
PR #38 → cf7f0f5939e75475ce10da14f932de1a7f33b257
PR #39 → 9e5b9c23467ff90a1c1452a255d4a6cfa245b6bf
PR #40 → 0b0709946e84e80918a0e50903badb8b7bd4fa12
PR #69 → bb940bf7d5a3b1f605b79e9fb8f33c463a8ee5a7
```

M8 Local Handoff execution subject:

```text
commit e7b4e23799a3579572598ebd5864a80831d49db4
tree   0b72b9f09f73d3829db2f138d457a5691641bf79
```

## Molecular implementation route

```text
#6 → #12 → #13 → #14
#14 → #36 → #42 → #44 → #45 → #51 → #52 → #65
#14 → #37 / #38 / #39 / #40
#39 → #55 / #56
#36 → #57
#40 → #58
```

Integration route:

```text
#68 backbone integration
#37/#38/#39/#40 path-disjoint main merges
#69 exact advanced runner tests/workflows convergence
M8 closure PR: README/AGENTS/milestones/registries/queue
```

PR #55–#58 are historical evidence subjects closed as integrated/superseded after their exact code and contract surfaces reached `main` through #68/#69.

## Runtime and Local Handoff route

```text
handoff/local-handoff-queue.json
  M8-LOCAL-REVIEWER-001         ACTIVE
    ↓ PASS receipt
  M8-LIVE-KIND-002              BLOCKED_BY_PREDECESSOR
    ↓ PASS receipt
  M8-COMPILE-ADVANCED-QUEUE-003 BLOCKED_BY_PREDECESSOR
    ↓ compile receipt + queue assertion + Human review
  generated M7 advanced queue   NOT_COMPILED
```

Current active command:

```bash
python3 scripts/handoff/run_local_reviewer_handoff.py \
  --output evidence/local-reviewer/handoff-receipt.json \
  --work-dir evidence/local-reviewer/work
```

## Open residual evidence

```text
DevOps #2  live kind/Kubernetes acceptance
DevOps #3  actual synthetic 1,000-VU run
DevOps #7  exact model artifact/local inference/live canary
DevOps #9  Local Handoff and advanced runtime convergence
DevOps #67 repository-admin cleanup of temporary branches
```

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow / Git Town / Local Handoff contracts |
| Manager routing | `ed3c/Product-Manager-Notes` | requirements, decisions, gaps and interview narrative |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | code, CI, failure/runtime evidence and receipts |
| Human projections | Google Sheet / Google Doc | dashboard and narrative only |

## Closure route

```text
requirement
→ invariant / system contract
→ implementation
→ deterministic or runtime oracle
→ negative control / failure
→ detection / authority / mitigation / recovery
→ corrective change
→ same-failure re-test
→ exact receipt
→ reviewer packet
→ main integration
→ Local Handoff for physical residuals
→ bounded claim
```

Missing edges remain `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`. Documentation, UI, issue state and PR state cannot fill a missing receipt.
