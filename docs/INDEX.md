# Documentation & Traceability Index

Machine/evidence authority remains with exact Git subjects, executable checks, Actions artifacts and admitted Local Handoff receipts. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_M9_LOCAL_RECEIPT_ADMISSION_READY.md
→ registry/public-m9-local-receipt-admission.json
→ registry/stack-plan.yaml
→ handoff/local-handoff-queue.json
→ exact issue / PR / current head / evidence head / workflow run / raw receipt / admitted packet
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
| M9 Local receipt admission | `docs/milestones/PUBLIC_M9_LOCAL_RECEIPT_ADMISSION_READY.md` | `registry/public-m9-local-receipt-admission.json` | `PASS_BOUNDED` |

## Current M9 Stack

```text
main @ 5d0c5db1626bf5c1a83334ea864b6a3eb7613df3
└─ A9 PR #77 feat/m9-local-receipt-admission
   │  exact hardened head fc7ae40c0a5ea0a403c2ed27555de3cbbc8d042b
   │  tree 67acc95ed6ee85091dfe30c8b853bc54203c3cda
   │  run 32376416583 SUCCESS
   └─ D9 docs/m9-local-receipt-admission-index
      issue #78
```

D9 is a true child because it consumes A9's unmerged admission contract. Local runtime receipts are process dependencies, not Git ancestry.

## M9 evidence route

```text
current Local Handoff queue
→ run only current ACTIVE item
→ raw typed receipt
→ scripts/handoff/admit_public_receipt_packet.py
   ├─ exact queue state/subject check
   ├─ exact receipt schema/verdict/ceiling/cleanup check
   ├─ blocked-future receipt rejection
   ├─ fixture/live separation
   ├─ receipt-root / size / sensitive-content guard
   └─ queue/raw-receipt overwrite guard
→ evidence/local-handoff/public-receipt-packet.json
→ Human/trusted queue review
→ deliberate queue advance or local gap
```

The public packet carries allowlisted summaries plus the raw receipt's root-relative path, SHA-256 and byte count. It does not copy arbitrary raw logs/output tails and does not independently reproduce the local run.

## Canonical Local Handoff frontier

Execution subject:

```text
commit e7b4e23799a3579572598ebd5864a80831d49db4
tree   0b72b9f09f73d3829db2f138d457a5691641bf79
```

Queue:

```text
M8-LOCAL-REVIEWER-001         ACTIVE
  ↓ raw receipt → M9 admission → trusted review
M8-LIVE-KIND-002              BLOCKED_BY_PREDECESSOR
  ↓ raw receipt → M9 admission → trusted review
M8-COMPILE-ADVANCED-QUEUE-003 BLOCKED_BY_PREDECESSOR
  ↓ compile receipt → M9 admission → portable assertion + trusted review
M7 advanced queue             NOT_COMPILED
```

Current first local command:

```bash
python3 scripts/handoff/run_local_reviewer_handoff.py \
  --output evidence/local-reviewer/handoff-receipt.json \
  --work-dir evidence/local-reviewer/work
```

After that receipt exists, public admission uses the authoritative M9 wrapper rather than the core library directly.

## Historical implementation route

```text
#6 → #12 → #13 → #14
#14 → #36 → #42 → #44 → #45 → #51 → #52 → #65
#14 → #37 / #38 / #39 / #40
#39 → #55 / #56
#36 → #57
#40 → #58

#68 backbone main integration
#37/#38/#39/#40 path-disjoint main merges
#69 exact advanced runner tests/workflows convergence
#70/#71 M8 routing and issue-closure integration
```

PR #55–#58 remain historical exact evidence/routing subjects after their code/tests reached `main` through convergence. No replay merge is needed solely to simplify diagrams.

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow / Git Town / Local Handoff contracts |
| Manager routing | `ed3c/Product-Manager-Notes` | requirements, decisions, gaps and interview narrative |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | code, CI, failure/runtime evidence, typed receipts and public receipt packets |
| Human projections | Google Sheet / Google Doc | dashboard and narrative only |

## Open residual evidence

```text
DevOps #2   live kind/Kubernetes acceptance
DevOps #3   actual synthetic 1,000-VU run
DevOps #7   exact model artifact/local inference/live canary
DevOps #9   physical Local Handoff and advanced runtime convergence
DevOps #67  repository-admin cleanup of temporary branches
DevOps #76  M9 receipt admission until merged to main
DevOps #78  M9 traceability until merged to main
```

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
→ exact raw receipt
→ exact-subject M9 admission
→ public-safe packet
→ Human/trusted routing decision
→ bounded claim
```

Missing edges remain `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`. Documentation, UI, issue state, PR state and packet existence cannot fill a missing physical receipt.
