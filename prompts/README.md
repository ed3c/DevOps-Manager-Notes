# Full Manager MVP Worker Prompt Router

This directory contains zero-context system prompts for separate ChatGPT/Agent sessions. The Tech Lead dispatches only after the exact subject and task contract are frozen.

## Dispatch order

```text
#11 / PR #12 technology + architecture contract
        ↓
#1 invariant/evidence audit
        ↓
#2 core platform contract
        ↓
┌────────────┬────────────┬────────────┬────────────┬────────────┐
#3           #4           #7           #8           #10
observability policy      llmops       console      supply-chain/fault
└────────────┴────────────┴────────────┴────────────┴────────────┘
        ↓ verified lane receipts
#5 failure/recovery convergence
        ↓ + #8 receipt
#9 final demo convergence
```

## Prompt files

- `issue-2-core-platform.md`
- `issue-3-observability-load.md`
- `issue-4-policy-security.md`
- `issue-7-llmops-progressive-delivery.md`
- `issue-8-demo-console.md`
- `issue-10-supply-chain-fault.md`
- `issue-5-failure-recovery.md`
- `issue-9-final-convergence.md`

## Required subject envelope

Before starting a fresh session, replace all placeholders with exact current values:

```yaml
repository: ed3c/DevOps-Manager-Notes
branch: <exact branch>
commit: <40-char SHA>
tree: <40-char tree SHA>
issue: ed3c/DevOps-Manager-Notes#N
base_or_parent: <exact branch/PR/commit>
allowed_paths: [...]
read_only_paths: [...]
forbidden_paths: [...]
start_dependencies: [...]
completion_dependencies: [...]
consumed_artifacts: [...]
expected_outputs: [...]
evidence_lane: <L2/L3/L4/L5>
evidence_ceiling: <explicit>
```

## Shared system laws

```text
MODE=MONITOR
```

- Read `AGENTS.md`, `docs/architecture/FULL_MVP_DEMO.md`, `registry/mvp-demo-stack.yaml`, and `registry/stack-plan.yaml` before writing.
- Source/README/tool presence is candidate information, not capability proof.
- Start-readiness and completion-readiness are distinct.
- Do not mutate outside the assigned path/resource lease.
- Do not invent shared interfaces; #2 owns the base typed API/artifact/evidence contract.
- FIRST_GREEN triggers Shadow Architect review.
- Every PASS binds exact subject, environment, workload and evidence lane.
- Every fault/retry/resource has a bound and cleanup obligation.
- `DRILL` is not production history; `1000 VU` is not real adoption; local K8s is not production tenure.
- Google Docs/Sheets have no evidence-promotion authority.
- Merge, force push, semantic conflict resolution, release, production promotion/rollback, visibility and permissions are Human/trusted-owner boundaries.

## Mandatory Shadow checkpoint output

For every material architecture delta record:

```text
delta class
what became newly possible
what must remain true
falsifier / oracle
intervention L0-L3
evidence impact
```

## Required handoff output

Every Worker finishes with a durable handoff summary:

```text
exact subject
files changed
artifacts consumed / produced
evals and negative controls run
receipt paths and verdicts
evidence ceiling
remaining NOT_IMPLEMENTED / NOT_EXERCISED
Shadow deltas
cleanup state
real blockers
whether Local Handoff is required
next legal task / prompt
Human-owned transitions
```

A Worker that reaches a genuine local-host boundary must stop and request/compile a typed Local Handoff item rather than claiming runtime completion.
