# Documentation & Traceability Index

Machine/evidence authority remains with exact registry subjects, executable checks, receipts, GitHub metadata and admitted runtime evidence. This file is navigation only.

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
→ exact issue / PR / commit / runtime receipt
```

## Current control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow Architect / Git Town reusable procedure |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe job/source/requirement/gap/prompt/narrative state |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI/runtime/failure evidence and public reviewer packet |
| Runtime contracts | `ed3c/runtime-env` when triggered | secret-free local/provider capability/workload contracts |
| External verification | `truth-verify-loop` / `openwiki-source-anchoring` when triggered | fresh claim/source verification without evidence promotion |
| Human dashboard | Google Sheet | non-authoritative mirror |
| Human narrative | Google Doc | non-authoritative mirror |

## Observed Full MVP subjects

```text
PR #6  bootstrap
└─ PR #12 / #11 Full MVP technology/architecture
   └─ PR #13 / #1 invariant/evidence audit
      └─ PR #14 / #2 Core remote FIRST_GREEN
         ├─ PR #36 / #3 observability/SLO/load             REMOTE_FIRST_GREEN
         ├─ PR #38 / #4 policy/security/license           REMOTE_FIRST_GREEN
         ├─ PR #39 / #7 ML/LLMOps/progressive delivery    REMOTE_FIRST_GREEN
         ├─ PR #37 / #8 Demo Console                      REMOTE_FIRST_GREEN
         └─ PR #40 / #10 supply-chain/fault               REMOTE_FIRST_GREEN

PR #36
└─ PR #42 / #5 failure/recovery/postmortem                 REMOTE_FIRST_GREEN
     ↑ exact side-input identities from #38 / #39 / #40

PR #42
└─ PR #44 / #9 reviewer convergence                        REMOTE_FIRST_GREEN
     ↑ exact Demo Console bytes from #37
     ↑ exact Actions artifacts from #36/#38/#39/#40/#42
```

M2, M3 and M4 remote checkpoints are `PASS_BOUNDED`; each has a distinct evidence ceiling.

## Current milestone subjects

### M2 — public remote fan-out

- `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md`
- `registry/public-m2-first-green.json`
- PRs `#36/#38/#39/#37/#40`

### M3 — public remote failure/recovery

- `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md`
- `registry/public-m3-failure-recovery.json`
- PR `#42`
- current PR head `c7e6a30af5b70bff6a7ac78eab2eb4bd0d46724e`
- admitted evidence head `e48711055572d83c872e72445cdf1389592ce85e`
- Actions run `32254018953`
- artifact `9365550423`
- artifact digest `sha256:098ba3e3427323c9c4651d5d8683d174723039d5fe32285045f95773d7419558`
- evidence ceiling `GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY`

### M4 — public reviewer convergence

- `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md`
- `registry/public-m4-reviewer-convergence.json`
- PR `#44`
- head `4ce77c5e0e4ece8379badea5c3fa477a3a463d62`

Primary artifact readback lane:

```text
workflow         Full MVP public reviewer convergence
run              32256405012
artifact         9366445128
digest           sha256:6acd3395bd198e46bd3c31da6a901371a5c2cfaf1552fbc3ee2bf77c53ddfdde
size             2,841,522 bytes
ceiling          GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY
```

Secondary deterministic replay lane:

```text
workflow         Full MVP reviewer convergence
run              32256405010
artifact         9366471049
digest           sha256:a6b17169bd1fe53122e27b934365fd8add7530e841541ce443637c5265758eef
size             1,394,199 bytes
ceiling          GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY
```

M4 is reviewer-demo-ready at the remote public ceiling, not production-ready.

## Architecture and stack

- `docs/architecture/FULL_MVP_DEMO.md` — end-to-end Internal AI Platform demo architecture, state machine, job coverage and failure path.
- `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md` — M2 fan-out PRs, runs, artifacts and residual proof obligations.
- `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md` — M3 seven-drill recovery closure and FIRST_GREEN hardening.
- `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md` — M4 artifact re-download, reviewer bundle, deterministic replay and BEFORE_PUBLIC_DEMO Shadow review.
- `registry/mvp-demo-stack.yaml` — selected permissive/commercial-use technology inventory and remaining proof.
- `registry/stack-plan.yaml` — observed/planned molecular Git Town Stack, Git ancestry, task convergence and path leases.
- `registry/public-m2-first-green.json` — machine-readable M2 execution index.
- `registry/public-m3-failure-recovery.json` — machine-readable M3 execution index.
- `registry/public-m4-reviewer-convergence.json` — machine-readable M4 reviewer convergence index.
- `scripts/demo/README.md` — bounded reviewer packet and one-command viewing contract.

## Evidence closure route

```text
source / requirement
→ invariant / architecture contract
→ molecular implementation leaves
→ exact lane receipts
→ failure / negative control
→ recovery + postmortem + corrective change
→ same-failure re-test
→ exact M3 receipt
→ exact artifact re-download + digest verification
→ bounded reviewer packet
→ deterministic replay smoke
→ exact M4 receipt
→ Product evidence graph / interview-safe narrative
```

A missing edge remains `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`; README/UI/issue state cannot fill it by assertion.

## Shadow M4 corrections

- Current PR head and artifact evidence head are separate subjects; PR #42 current head does not retroactively relabel the admitted M3 artifact.
- M4 re-downloads and verifies the six exact M2/M3 artifact archives before admission.
- The two PR #44 workflows have different evidence obligations: artifact readback/bundle assembly versus deterministic fresh replay. Neither may promote the other's ceiling.
- Public reviewer bundles are size-bounded and secret-pattern checked before persistence.

## Local Handoff

`handoff/local-handoff-queue.json` is the zero-context local continuation surface. Queue validity proves shape only. Every executable item binds an exact commit/tree, bounded command, sanitized receipt and PASS exit condition.

M4 remains below live/full runtime closure. Live kind/Kubernetes, local model/llama.cpp, real Argo CD/Rollouts, 1,000-VU recovery and substrate-specific recovery claims require typed Local Handoff or independently admitted runtime receipts.

## Next owner

```text
M4 bounded public reviewer packet
+
optional higher-substrate Local Handoff receipts
→ Product-Manager-Notes final interview/evidence convergence
```

Merge/release/production/visibility and real-experience claims remain Human-owned.
