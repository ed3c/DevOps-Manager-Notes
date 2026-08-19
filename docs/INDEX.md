# Documentation & Traceability Index

Machine/evidence authority remains with exact registry subjects, executable checks, receipts, GitHub metadata and admitted runtime evidence. This file is navigation only.

## Start here

```text
README.md
→ AGENTS.md
→ docs/architecture/FULL_MVP_DEMO.md
→ docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md
→ docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md
→ registry/mvp-demo-stack.yaml
→ registry/stack-plan.yaml
→ registry/public-m2-first-green.json
→ registry/public-m3-failure-recovery.json
→ prompts/README.md
→ exact issue / PR / commit / runtime receipt
```

## Current control planes

| Plane | Owner | Purpose |
|---|---|---|
| Method | `ed3c/skills-shared` | Tech Lead / Shadow Architect / Git Town reusable procedure |
| Manager routing | `ed3c/Product-Manager-Notes` | public-safe job/source/requirement/gap/prompt/narrative state |
| Executable evidence | `ed3c/DevOps-Manager-Notes` | implementation, CI/runtime/failure evidence and public Demo Console |
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

PR #42 exact receipt + PR #37 UI receipt
└─ #9 final reviewer convergence                            NOT_IMPLEMENTED
```

M2 remote fan-out checkpoint and M3 failure/recovery checkpoint are both `PASS_BOUNDED`. Exact subjects live in the two machine registries and milestone documents.

## Current milestone subjects

### M2 — public remote fan-out

- `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md`
- `registry/public-m2-first-green.json`
- PRs `#36/#38/#39/#37/#40`

### M3 — public remote failure/recovery

- `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md`
- `registry/public-m3-failure-recovery.json`
- PR `#42`
- head `e48711055572d83c872e72445cdf1389592ce85e`
- Actions run `32254018953`
- artifact `9365550423`
- artifact digest `sha256:098ba3e3427323c9c4651d5d8683d174723039d5fe32285045f95773d7419558`
- evidence ceiling `GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY`

M3 exercises seven bounded DRILL scenarios with recovery and same-failure re-test. It is not production incident history.

## Architecture and stack

- `docs/architecture/FULL_MVP_DEMO.md` — end-to-end Internal AI Platform demo architecture, state machine, job coverage and failure path.
- `docs/architecture/DELIVERY_RELIABILITY_LAB.md` — base reliability contract.
- `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md` — M2 fan-out PRs, runs, artifacts, Shadow deltas and residual proof obligations.
- `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md` — M3 seven-drill recovery closure, FIRST_GREEN hardening and residual proof obligations.
- `registry/mvp-demo-stack.yaml` — selected permissive/commercial-use technology inventory and remaining proof.
- `registry/stack-plan.yaml` — observed/planned molecular Git Town Stack, Git ancestry, task convergence and path leases.
- `registry/public-m2-first-green.json` — machine-readable M2 execution index.
- `registry/public-m3-failure-recovery.json` — machine-readable M3 execution index.
- `prompts/README.md` — zero-context Worker router for separate ChatGPT/Agent sessions.

## Failure / recovery proof route

```text
exact M2 receipt subjects
→ bounded failure trigger
→ declared detector
→ incident role / authority
→ mitigation
→ recovery verification
→ postmortem
→ corrective change
→ same-failure re-test
→ exact M3 receipt
```

Seven current drill classes:

```text
FR-01 bad release regression
FR-02 dependency timeout
FR-03 queue saturation/backpressure
FR-04 duplicate-side-effect/idempotency
FR-05 permission failure
FR-06 observability blind spot
FR-07 restore/DR assumption
```

A missing edge remains `ABSENT`, `NOT_IMPLEMENTED` or `NOT_EXERCISED`; README/UI/issue state cannot fill it by assertion.

## Shadow M3 corrections

The first #42 green run was not treated as terminal closure. Shadow review corrected an evidence-summary shell/heredoc defect, removed the false #8→#5 dependency edge, added Python environment identity, preserved `side_input_artifact_redownload=NOT_EXERCISED`, and hardened semantic drill assertions. The hardened run is the M3 subject recorded above.

## Local Handoff

`handoff/local-handoff-queue.json` is the zero-context local continuation surface. Queue validation proves shape only. Every executable item binds an exact commit/tree, bounded command, sanitized receipt and PASS exit condition.

M3 remains below live/full runtime closure. Live kind/Kubernetes, local model/llama.cpp, live Argo Rollouts/Prometheus canary, 1,000-VU recovery and substrate-specific recovery claims require typed Local Handoff or independently admitted runtime receipts.

## Next owner

```text
M2 exact lane receipts
+
M3 PR #42 failure/recovery receipt
+
PR #37 Demo Console receipt
→ #9 final reviewer convergence
```

#9 must produce one bounded deterministic reviewer entrypoint while keeping all local/substrate/production gaps explicit. Merge/release/production and real-experience claims remain Human-owned.
