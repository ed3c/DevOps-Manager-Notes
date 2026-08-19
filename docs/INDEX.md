# Documentation & Traceability Index

Machine/evidence authority remains with exact registry subjects, executable checks, GitHub Actions artifacts, receipts, GitHub metadata and admitted runtime evidence. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md
→ docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md
→ docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md
→ registry/mvp-demo-stack.yaml
→ registry/stack-plan.yaml
→ registry/public-m2-first-green.json
→ registry/public-m3-failure-recovery.json
→ registry/public-m4-reviewer-convergence.json
→ prompts/README.md
→ exact issue / PR / commit / Actions run / artifact / Local Handoff receipt
```

## Control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow Architect / Git Town reusable procedure |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe job/source/requirement/gap/prompt/narrative state |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI/runtime/failure evidence and public reviewer packet |
| Runtime contracts | `ed3c/runtime-env` when triggered | secret-free local/provider capability/workload contracts |
| External verification | `truth-verify-loop` / `openwiki-source-anchoring` when triggered | fresh claim/source verification without evidence promotion |
| Google Doc/Sheet | non-authoritative projection | human narrative/dashboard only |

## Observed Full MVP Stack

```text
PR #6  bootstrap
└─ PR #12 / #11 Full MVP technology/architecture
   └─ PR #13 / #1 invariant/evidence audit
      └─ PR #14 / #2 Core remote FIRST_GREEN
         ├─ PR #36 / #3 observability/SLO/load             M2 PASS_BOUNDED
         ├─ PR #38 / #4 policy/security/license           M2 PASS_BOUNDED
         ├─ PR #39 / #7 ML/LLMOps/progressive delivery    M2 PASS_BOUNDED
         ├─ PR #37 / #8 Demo Console                      M2 PASS_BOUNDED
         └─ PR #40 / #10 supply-chain/fault               M2 PASS_BOUNDED

PR #36
└─ PR #42 / #5 failure/recovery/postmortem                 M3 PASS_BOUNDED
     ↑ exact evidence identities from #38 / #39 / #40

PR #42
└─ PR #44 / #9 reviewer convergence                        M4 PASS_BOUNDED
     ↑ exact Demo Console bytes from #37
     ↑ six exact M2/M3 Actions archives re-downloaded + verified
     └─ PR #45 Local Handoff Queue                         ACTIVE / NOT_EXECUTED
```

Task-DAG convergence and Git ancestry are separate. A convergence node has one real Git parent; other prerequisites are typed byte/evidence/process side inputs.

## M2 — public remote fan-out

Canonical:

- `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md`
- `registry/public-m2-first-green.json`
- PRs `#36/#38/#39/#37/#40`

This stage proves only the lane-specific remote ceilings recorded in those artifacts.

## M3 — public remote failure/recovery

Canonical:

- `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md`
- `registry/public-m3-failure-recovery.json`
- PR `#42`

Exact admitted M3 evidence:

```text
evidence head    e48711055572d83c872e72445cdf1389592ce85e
Actions run      32254018953
artifact         9365550423
digest           sha256:098ba3e3427323c9c4651d5d8683d174723039d5fe32285045f95773d7419558
scenario count   7 DRILLs
ceiling          GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY
```

PR #42's mutable current head is separately tracked; it does not replace the historical evidence subject.

## M4 — public reviewer convergence

Canonical:

- `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md`
- `registry/public-m4-reviewer-convergence.json`
- PR `#44`
- source head `55d18cdc556ca5d66c67406318ae25196c077fd2`
- source tree `a4ad37d9baf73a5239f79c516c67b0182420336a`

### Deterministic reviewer replay

```text
run              32256802856
artifact         9366615717
digest           sha256:e652cdf3ccb8de7a8655f9148bc6471a29bcaeaef2d55f6255bca2cb2b1e19d3
size             1,394,198 bytes
ceiling          GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY
```

Proves exact Demo Console byte parity, current PR-head readback, one-command deterministic reviewer execution, seven DRILL replays, business PASS/FAIL telemetry, same-failure re-test and no paid API dependency.

### Exact Actions artifact re-verification

```text
run              32256802554
artifact         9366596481
digest           sha256:696f56be2fb637e386941eb313caa7c9448900ad0bad88b3a96119b95315596c
size             2,841,522 bytes
ceiling          GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY
```

This independently re-downloads the six exact M2/M3 Actions archives, verifies their SHA-256 identities and admits only required public-safe files into the reviewer packet.

## Local Handoff

PR #45 is the Local Handoff child of PR #44. Exact source:

```text
commit           55d18cdc556ca5d66c67406318ae25196c077fd2
tree             a4ad37d9baf73a5239f79c516c67b0182420336a
active item      M4-LOCAL-REVIEWER-001
```

Command:

```bash
bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
```

Expected receipt:

```text
evidence/local-reviewer/reviewer-demo-receipt.json
```

The next live-substrate item is `BLOCKED_UNRESOLVED`. No command for kind/Kubernetes, Argo, Qwen/llama.cpp or 1,000 VU becomes executable until a committed bounded runner, exact artifacts, resource budget and cleanup contract exist.

## Evidence closure route

```text
source / requirement
→ invariant / product-system contract
→ technology ADR
→ Tech Lead task contract
→ molecular implementation leaf
→ deterministic/runtime oracle
→ failure / negative control
→ mitigation / recovery
→ corrective change
→ same-failure re-test
→ exact lane receipt
→ exact Actions artifact re-download / verification
→ bounded reviewer packet
→ Local Handoff for higher substrate proof
→ Product evidence graph / interview-safe narrative
```

A missing edge remains `ABSENT`, `NOT_IMPLEMENTED`, `NOT_EXERCISED` or `HUMAN_ADMIT_REQUIRED`; README, issue, PR, UI or queue state cannot fill it by assertion.

## Remaining proof ceiling

```text
live kind/Kubernetes                         NOT_EXERCISED
real Argo CD reconciliation                  NOT_EXERCISED
live Argo Rollouts + Prometheus canary       NOT_EXERCISED
local Qwen / llama.cpp                       NOT_EXERCISED
1,000-VU capacity / recovery                 NOT_EXERCISED
registry-stored image signing                NOT_EXERCISED
production users / incidents / tenure        OUTSIDE_REPOSITORY_PROOF
```

Remote M4 is stage-complete. Further evidence promotion requires an exact Local Handoff/runtime receipt or Human-owned admission.
