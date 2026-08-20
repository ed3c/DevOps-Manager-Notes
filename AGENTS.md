# AGENTS.md

## Purpose

This public repository is the executable evidence plane for the Full Manager MVP Demo. It must remain independently reviewable without access to the private `Product-Manager-Notes` control plane.

`Product-Manager-Notes` owns source/requirement/gap/orchestration/narrative state. `skills-shared` owns reusable methods. This repository owns implementation, runtime/failure proof, exact receipts, public-safe Demo Console and delivery evidence.

## Mandatory read order

1. `README.md`
2. `docs/INDEX.md`
3. `docs/architecture/FULL_MVP_DEMO.md`
4. `roles/devops-manager/job-contract.yaml`
5. `registry/mvp-demo-stack.yaml`
6. `registry/evidence.yaml`
7. `registry/gaps.yaml`
8. `registry/stack-plan.yaml`
9. `prompts/README.md`
10. exact issue / PR / commit / Local Handoff subject
11. nearest directory README/contract/test/receipt when it exists

When reusable procedure is needed, read the canonical owners in `ed3c/skills-shared`:

```text
skills/agentic-tech-lead-orchestration/
skills/spatial-loop-systems-engineering/
skills/git-town-stacked-pr-worker/
```

Trigger-selected support only:

```text
runtime-env                when a secret-free runtime/profile/workload contract is needed
truth-verify-loop          when a mutable/high-risk external claim needs fresh verification
openwiki-source-anchoring  when generated documentation/source claims need exact source anchoring
skill-resume-site          only for admitted public portfolio export
```

No support repository may own this repository's mutable issue/branch/runtime state or widen authority.

## Operating mode

Default `MODE=MONITOR`.

Builder may perform reversible design, code, tests and bounded execution. In parallel, Shadow Architect watches material deltas:

```text
ASSUMPTION
STATE
AUTHORITY
OWNERSHIP
LIFECYCLE
CONCURRENCY
RESOURCE
EXTERNAL_SIDE_EFFECT
FAILURE_SURFACE
EVIDENCE
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

L3 is reserved for unsafe/irreversible transitions, secret/private exposure, destructive migration without rollback, privilege expansion, unbounded fault injection, semantic conflict, evidence laundering or public claim inflation.

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

Start-readiness and completion-readiness are separate edge classes. A task may start with bounded unknowns, but it cannot close without its own exact receipt and all completion predecessors.

Every stage/session handoff records:

```text
repository / branch / commit / tree / issue
state_in / state_out
goal / non-goals
allowed / read-only / forbidden paths
runtime resources and lease owner
consumed / produced artifacts
start dependencies / completion dependencies
invariants / negative controls
evidence state / evidence ceiling
Shadow deltas + intervention level
unknowns / blockers
local runtime handoff required?
next prompt / stage
Human-owned operations
```

## Tech Lead laws

- Freeze exact subject, objective, non-goals, invariants, dependencies, acceptance criteria, budgets, rollback and evidence lane before fan-out.
- A task dependency exists only for real artifact/state consumption or an admitted completion receipt.
- A Git true-child exists only when the child consumes the parent's **unmerged bytes/contracts**.
- Parallel writers require disjoint file/resource leases.
- Worker/LLM/issue/branch/CI/process self-report is candidate evidence only.
- Every deployment side effect has rollback/reconciliation semantics.
- Every retry path has idempotency and a bounded retry budget.
- Every growing resource has a bound or saturation oracle.
- Every performance claim names workload, environment, percentile/window, duration and evidence lane.
- FIRST_GREEN triggers Shadow review; it never closes the manager proof loop.
- Synthetic incidents are `DRILL`/`SIMULATION`.
- 1,000 virtual users are not 1,000 real users.
- Local Kubernetes is not production-cluster experience.
- UI state cannot promote backend evidence state.

## Full MVP shared contracts

PR #12 / issue #11 freezes the current Full MVP technology/design contract. It is design evidence, not runtime proof.

The base implementation owner #2 must freeze these shared interfaces before fan-out:

```text
typed API schema
business oracle contract
artifact identity contract
deployment revision contract
evidence receipt envelope
health/readiness semantics
local namespace / cluster naming
rollback target contract
```

Until #2 freezes them, #3/#4/#7/#8/#10 may inspect/design but must not independently invent incompatible shared interfaces.

## Molecular Git Town / Worker laws

Follow `git-town-stacked-pr-worker`:

```text
PATH-DISJOINT + no unmerged consumption → SIBLING
consumes parent unmerged bytes/contract → TRUE_CHILD
smallest behavior + tests + evidence    → TERMINAL_LEAF
shared multi-input closure              → CONVERGENCE
physical runtime prerequisite           → PROCESS_DEPENDENCY / LOCAL_HANDOFF
```

Atom vocabulary:

```text
C contract/schema/interface lock
K deterministic core
A adapter/provider/substrate
E eval/mutation/failure control
X convergence/E2E
D docs/receipt/handoff
```

Never invent branch names, PR numbers, head SHAs, merged state or multi-parent Git ancestry. `registry/stack-plan.yaml` is the consumer-owned machine plan and must be updated from observed GitHub metadata.

## Current Worker leases

After #2 freezes the shared service/artifact interfaces, the intended parallel lanes are:

```text
#3  observability/, sre/, tests/load/, evidence/receipts/observability/
#4  platform/policies/, tests/failure/policy/, evidence/receipts/security/
#7  mlops/, platform/rollouts/, evidence/receipts/llmops/
#8  demo-console/ and its tests only
#10 supply-chain/, bounded fault-tool tests, evidence/receipts/supply-chain/
```

These are siblings only while they consume the same frozen #2 contracts and do not consume each other's unmerged bytes. Reclassify real ancestry if that changes.

Shared final surfaces have one convergence owner:

```text
#5 owns incidents/runbooks/management/failure receipts for the reliability convergence.
#9 owns final README/index/demo orchestration/convergence receipt after prerequisite closure.
```

## Technology admission

`registry/mvp-demo-stack.yaml` is the selected stack inventory. Default distribution prefers permissive families (MIT, Apache-2.0, BSD, PostgreSQL-style) and avoids forced source disclosure by default.

Top-level repository licensing is not recursive clearance. Treat these as separate subjects:

```text
Python transitive packages
npm transitive packages
container base images
Kubernetes/Argo/MLflow/Jaeger/Prometheus images
plugins/exporters
GitHub Actions / marketplace actions
model weights/tokenizers
hosted/proprietary service terms
```

Every downloaded model/image/tool artifact requires its own digest and license record before demo admission.

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

Lower evidence never self-promotes. Exact PASS binds subject, revision, workload, environment and evidence lane.

## Closure rule

A technical manager capability closes only through:

```text
requirement
→ architecture / invariant
→ implementation
→ business/SLI/SLO oracle
→ negative control / failure injection
→ incident decision + mitigation/recovery
→ corrective change
→ same-failure repeated verification
→ durable exact-subject receipt
```

A successful deployment without a failure/recovery proof is incomplete Manager evidence.

## Local Handoff Execution Queue

Use `handoff/local-handoff-queue.json` only at a genuine local host/runtime/provider/forge boundary.

Every ACTIVE item binds:

```text
exact target commit + tree
required capabilities
concrete argv + cwd + timeout
sanitized durable receipt
required PASS exit
cleanup obligation
next item, if one already has an executable command
```

Do not put secrets, credential values, private reasoning or generic arbitrary shell commands in a queue. Do not create a placeholder future command just to make the queue look complete. Compile the next item only after its executable runner exists.

Queue shape validation is not execution. Local capability PASS does not prove application/Kubernetes/model/fault correctness.

## Google / GitHub boundary

GitHub is the canonical public evidence surface here. Product control-plane Google Sheet/Doc are human mirrors only. This public repo must never depend on a private URL to explain its evidence.

## Automation boundary

Unattended workers may create/update bounded code/docs/tests, run deterministic CI, emit receipts and prepare draft PRs when contracts allow it. They must stop on:

```text
stale/wrong subject
overlapping writer/resource lease
missing predecessor receipt
semantic conflict
required local capability unavailable
secret/private disclosure risk
unbounded retry/resource/fault injection
invalid/mismatched receipt
failed cleanup
Human-owned transition
```

The following remain Human/trusted-owner operations:

```text
semantic conflict resolution
force push / merge / release
repository visibility / permission widening
production promotion / production rollback admission
credential/provider enrollment
claims of real users, real incidents, production tenure or people-management tenure
```
