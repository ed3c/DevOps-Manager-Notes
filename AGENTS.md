# AGENTS.md

## Purpose

This public repository is the executable evidence plane for the Full Manager MVP Demo. It must remain independently reviewable and public-safe.

`Product-Manager-Notes` is the public-safe Manager requirement/routing/narrative plane. `skills-shared` owns reusable Tech Lead, Shadow Architect and Git Town methods. This repository owns implementation, CI/runtime/failure evidence, exact receipts, the Demo Console, reviewer convergence and the typed Local Handoff queue.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `docs/milestones/PUBLIC_REMOTE_FANOUT_FIRST_GREEN.md`
5. `docs/milestones/PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN.md`
6. `docs/milestones/PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN.md`
7. `roles/devops-manager/job-contract.yaml`
8. `registry/mvp-demo-stack.yaml`
9. `registry/evidence.yaml`
10. `registry/gaps.yaml`
11. `registry/stack-plan.yaml`
12. `registry/public-m2-first-green.json`
13. `registry/public-m3-failure-recovery.json`
14. `registry/public-m4-reviewer-convergence.json`
15. `handoff/local-handoff-queue.json` when crossing the local/runtime boundary
16. `prompts/README.md`
17. exact issue / PR / commit / Actions run / artifact / receipt
18. nearest directory README/contract/test/receipt when it exists

Reusable procedure must be read from canonical `ed3c/skills-shared` owners rather than copied into local variants:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Trigger-selected support only:

```text
runtime-env                secret-free runtime/profile/workload contract
truth-verify-loop          mutable/high-risk external claim verification
openwiki-source-anchoring  exact source/path/quote anchoring
skill-resume-site          admitted public portfolio projection only
```

No support repository becomes a second mutable authority for this repo.

## Operating mode

Default `MODE=MONITOR`.

Builder may perform reversible design/code/tests and bounded execution. Shadow Architect independently watches:

```text
ASSUMPTION_DELTA
STATE_DELTA
AUTHORITY_DELTA
OWNERSHIP_DELTA
LIFECYCLE_DELTA
CONCURRENCY_DELTA
RESOURCE_DELTA
EXTERNAL_SIDE_EFFECT_DELTA
FAILURE_SURFACE_DELTA
EVIDENCE_DELTA
```

For every material delta ask:

1. What became newly possible?
2. What must now remain true?
3. How would we know it is false?

Intervention:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

L3 includes unsafe/irreversible changes, secret/private disclosure, destructive migration without rollback, privilege expansion, unbounded fault injection, overlapping mutation authority, semantic conflict, evidence laundering or public claim inflation.

## Current checkpoints

```text
M1 CORE_REMOTE_FIRST_GREEN                        PASS_BOUNDED
M2 PUBLIC_REMOTE_FANOUT_FIRST_GREEN               PASS_BOUNDED
M3 PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN     PASS_BOUNDED
M4 PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN PASS_BOUNDED
```

M4 remote reviewer evidence is bound to PR #44 source:

```text
commit 55d18cdc556ca5d66c67406318ae25196c077fd2
tree   a4ad37d9baf73a5239f79c516c67b0182420336a
```

Remote evidence ceilings remain separate:

```text
GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY
GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY
```

These do not prove live Kubernetes, real Argo runtime, local model inference, 1,000-VU recovery, production users/incidents or management tenure.

## Eight-stage execution contract

```text
P0 SUBJECT_AUTHORITY
→ P1 SOURCE_EVIDENCE
→ P2 PROBLEM_CLOSURE_SYSTEM_DESIGN
→ P3 TECHNOLOGY_ADR
→ P4 TECH_LEAD_STACK_PLAN
→ P5 PARALLEL_IMPLEMENTATION
→ P6 SHADOW_RUNTIME_FAILURE
→ P7 CONVERGENCE_HANDOFF
```

Start-readiness and completion-readiness are distinct. A task may start with bounded unknowns but cannot close without its own receipt and all completion predecessors.

Every zero-context handoff records:

```text
repository / branch / commit / tree / issue
state_in / state_out
goal / non-goals
allowed / read-only / forbidden paths
resource leases
consumed / produced artifacts
start / completion dependencies
invariants / negative controls
evidence state / ceiling
Shadow deltas / intervention
unknowns / blockers
Local Handoff requirement
next prompt / stage
Human-owned operations
```

## Tech Lead laws

- Freeze exact subject, objective, non-goals, invariants, dependencies, acceptance criteria, budgets, rollback and evidence lane before fan-out.
- Dependency edges require real artifact/state consumption or an admitted receipt.
- Git ancestry and task-DAG dependencies are separate graphs.
- Parallel writers require disjoint path/resource leases; observed lease deltas must be recorded.
- Worker/LLM/issue/branch/process/CI self-report is candidate evidence only.
- Every deployment side effect has rollback/reconciliation semantics.
- Retry paths require idempotency and bounded retry budgets.
- Growing resources require bounds or saturation oracles.
- Performance claims name workload/environment/window/duration/evidence lane.
- FIRST_GREEN triggers Shadow review; it never closes production proof.
- Synthetic incident evidence remains `DRILL`/`SIMULATION`.
- 1,000 virtual users are synthetic load evidence, not 1,000 real users.
- Local Kubernetes is not production-cluster experience.
- UI state cannot promote backend evidence.
- Queue existence cannot promote local execution.

## Evidence subject law

A mutable PR head and a historical artifact evidence head are different subjects.

```text
current_head
  = current mutable branch/PR routing subject

evidence_head
  = exact commit that produced the admitted workflow artifact
```

Never relabel an older Actions artifact as evidence for a newer head.

For PR #42, the admitted M3 split is intentional:

```text
current PR head   c7e6a30af5b70bff6a7ac78eab2eb4bd0d46724e
evidence head     e48711055572d83c872e72445cdf1389592ce85e
evidence artifact 9365550423
```

## Molecular Git Town laws

Follow `git-town-stacked-pr-worker`:

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical/local prerequisite             → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Observed current Stack:

```text
PR #14 Core
├─ PR #36 Observability
├─ PR #38 Policy/Security
├─ PR #39 ML/LLMOps
├─ PR #37 Demo Console
└─ PR #40 Supply/Fault

PR #36
└─ PR #42 Failure/Recovery
     ↑ exact evidence side inputs #38/#39/#40

PR #42
└─ PR #44 Reviewer Convergence
     ↑ exact Demo Console bytes #37
     ↑ exact M2/M3 Actions artifacts
     └─ PR #45 Local Handoff Queue
```

Never fabricate multi-parent Git history. One convergence owner chooses one real Git base and consumes other prerequisites as typed side inputs.

## M4 reviewer convergence laws

Issue #9 / PR #44 has two intentionally distinct proof lanes:

```text
full-reviewer-demo.yml
→ exact Demo Console byte parity
→ current PR-head readback
→ deterministic reviewer bootstrap
→ seven DRILL replays
→ business PASS/FAIL telemetry

full-reviewer-convergence.yml
→ six exact Actions artifact re-downloads
→ SHA-256 archive verification
→ required-path admission
→ bounded static reviewer bundle
```

The two workflows must not promote each other's evidence ceiling. If their proof obligations become identical, collapse them into one owner.

The deterministic developer entrypoint is:

```bash
bash scripts/demo/run_reviewer_demo.sh <output-directory>
```

It has no paid model/provider API dependency. It is still not live-substrate proof.

## Local Handoff

PR #45 owns the current typed Local Handoff leaf. Queue subject:

```text
commit 55d18cdc556ca5d66c67406318ae25196c077fd2
tree   a4ad37d9baf73a5239f79c516c67b0182420336a
```

ACTIVE item:

```text
M4-LOCAL-REVIEWER-001
```

Command:

```bash
bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
```

Expected receipt:

```text
evidence/local-reviewer/reviewer-demo-receipt.json
```

Evidence ceiling:

```text
LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY
```

The next item `M4-LIVE-SUBSTRATE-002` is `BLOCKED_UNRESOLVED`. Do not invent kind/Kubernetes, Argo, Qwen/llama.cpp or 1,000-VU commands. First commit a bounded runner with exact tool/model/image subjects, resource limits, timeouts, cleanup and receipt schema; only then make the queue item executable.

## Evidence states and ladder

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

```text
L0 SOURCE_CLAIM
L1 STATIC_REASONING
L2 DETERMINISTIC_TEST
L3 LOCAL_INTEGRATION
L4 REAL_SUBSTRATE
L5 ADVERSARIAL_OR_CHAOS
L6 PRODUCTION_OBSERVATION
```

Lower evidence never self-promotes.

Forbidden promotions include:

```text
CI_GREEN               → BUSINESS_CORRECT
REMOTE_FIRST_GREEN     → PRODUCTION_RUNTIME
LOCAL_REVIEWER_PASS    → LIVE_K8S_PASS
LOCAL_K8S_PASS         → PRODUCTION_INFRA_EXPERIENCE
1000_VU_PASS           → 1000_REAL_USERS
DRILL_COMPLETE         → PRODUCTION_INCIDENT_HISTORY
LICENSE_METADATA_PASS  → BLANKET_LEGAL_CLEARANCE
UI_GREEN               → BACKEND_EVIDENCE_PASS
ISSUE_CLOSED           → RUNTIME_CLOSED
CURRENT_PR_HEAD         → HISTORICAL_ARTIFACT_EVIDENCE
QUEUE_EXISTS            → QUEUE_EXECUTED
```

## Public disclosure stop law

Before public artifact persistence or portfolio projection, stop if any output contains or could expose:

```text
credentials / private keys / tokens
customer or user private data
employer/client confidential material
private repository source/body content
restricted paid/source material
unredacted machine/user identifiers
claims above the admitted evidence ceiling
```

Public repo reachability itself is never proof of safety or capability.

## Human-owned operations

Do not automate:

```text
semantic merge-conflict resolution
force push
merge / release
repository visibility or permission changes
production promotion / rollback admission
claiming real users / incidents / production experience
claiming people-management or TPM tenure
```

Stop on stale subjects, overlapping leases, invalid receipts, unavailable physical runtime, unbounded side effects, semantic conflicts or any Human-owned transition.
