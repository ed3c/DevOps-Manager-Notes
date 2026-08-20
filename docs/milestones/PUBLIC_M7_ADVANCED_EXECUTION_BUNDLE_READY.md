# M7 — PUBLIC_ADVANCED_EXECUTION_BUNDLE_READY

Status: `PASS_BOUNDED`

M7 converts the four independent M6 advanced runner contracts into one exact, reviewable execution bundle and a receipt-gated compiler for the **next** canonical Local Handoff epoch. It does not execute the physical runtime lanes.

## Exact implementation subject

```text
Issue:          #60
PR:             #65
branch:         handoff/m7-advanced-runtime-bundle
base:           handoff/m5-live-kind-queue / PR #52
head:           cf63e2fc85d56c2e49cfefd33fefbec30316e1fa
tree:           7dce94e01dd3630662deb6dfb3c67c8b5f272bb0
contract run:   32275551599
result:         SUCCESS
```

Evidence ceiling:

```text
GITHUB_HOSTED_M7_ADVANCED_BUNDLE_AND_QUEUE_COMPILER_ONLY
```

## True dependency shape

PR #65 has one real Git parent: canonical queue PR #52. Advanced implementation bytes are typed side inputs with exact parity checks:

```text
PR #52 canonical Local Handoff
└─ X7 PR #65 advanced execution bundle
     ↑ PR #55 Argo @ 8d976171f4aa2eba72bee360823b660f9bed99d4
     ↑ PR #56 model @ 63355992f382cf260c624e2c7c7c3733cce82c20
     ↑ PR #57 capacity @ 2240e8ee7ae9f151503d5c03d8043938dbbdce95
     ↑ PR #58 registry signing @ 1b543fdfad73377fa6ba51e3f190b56ed60452fa
```

The CI reads all imported runner paths back from those exact subjects and compares bytes. No fake multi-parent Git ancestry is created.

## Shadow lifecycle correction

M7 dependency analysis found that the original advanced Argo contract expected an existing `kind-manager-demo-*` context, while the M5 live-kind runner intentionally deletes its cluster during cleanup. That was a false lifecycle dependency.

PR #55 was hardened to current subject:

```text
head  8d976171f4aa2eba72bee360823b660f9bed99d4
tree  fada58f36c83de296decb41dcd34531b9d73145a
run   32274548200 PASS
```

Its current self-contained runner now owns one scoped ephemeral kind cluster:

```text
exact kind node image digest
→ refuse existing manager-demo-* cluster
→ capture caller kubectl context
→ create one ephemeral kind cluster
→ run exact Argo controller install contract
→ require inner receipt + cleanup PASS
→ delete attempted cluster
→ restore caller context
```

Highest future evidence remains `LOCAL_ARGO_CONTROLLERS_READY_ONLY`; no Application reconciliation or live canary is inferred.

## Receipt-gated compiler

`compile_m7_advanced_queue.py` requires both real predecessor receipts before a live advanced queue can be emitted.

Canonical predecessor execution epoch:

```text
commit 4cc3e162c00a3af240bab9e62482e07bb3e4f9a1
tree   5ff3349c1eb5c7976263c2e89347a353ccbc1072
```

Required live receipts:

```text
reviewer:
  schema  full-manager-mvp/local-reviewer-handoff-receipt/v1
  state   PASS
  ceiling LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY

kind:
  schema  full-manager-mvp/local-kind-substrate-receipt/v1
  verdict PASS
  ceiling LOCAL_KIND_KUBERNETES_APPLICATION_SMOKE_ONLY
```

The compiler rejects absent, FAIL, wrong-subject and wrong-ceiling receipts.

### Fixture isolation

Test receipts are labeled:

```text
evidence_kind = FIXTURE
```

They are accepted only with explicit `--fixture-mode`. A fixture is rejected in live mode. Fixture compilation writes a compile receipt with:

```text
evidence_kind             FIXTURE
physical_runtime_executed false
evidence_ceiling          FIXTURE_COMPILER_CONTRACT_ONLY
```

Fixtures validate compiler behavior only.

## Future advanced queue order

The compiler produces canonical `agentic-tech-lead/local-handoff-queue/v1` vocabulary with exactly one ACTIVE item:

```text
M7-ARGO-CONTROLLERS-001       ACTIVE
        ↓ PASS + cleanup
M7-LOCAL-MODEL-002            BLOCKED_BY_PREDECESSOR
        ↓ PASS + cleanup
M7-CAPACITY-003               BLOCKED_BY_PREDECESSOR
        ↓ PASS + cleanup
M7-REGISTRY-SIGNING-004       BLOCKED_BY_PREDECESSOR
```

The queue is intentionally sequential. This prevents overlapping local cluster/model/load/registry resource ownership and keeps completion-readiness receipt-gated.

Potential real-PASS ceilings remain independent:

```text
Argo      LOCAL_ARGO_CONTROLLERS_READY_ONLY
Model     LOCAL_LLAMA_CPP_MODEL_INFERENCE_ONLY
Capacity  LOCAL_SYNTHETIC_1000_VU_ONLY
Signing   LOCAL_REGISTRY_STORED_IMAGE_SIGNATURE_ONLY
```

## Contract CI evidence

Run `32275551599` passed:

```text
exact runner byte parity                    PASS
compiler/runners compile                    PASS
receipt admission negative controls         7/7 PASS
fixture queue one-ACTIVE topology           PASS
portable Local Handoff assertion            PASS
portable negative-control selftest           PASS
fixture physical_runtime_executed=false     PASS
secret-like fixture/compiler scan           PASS
```

Two intermediate red runs remain visible:

```text
32275347591  test expectation used wrong capacity argv index
32275449122  no-runtime assertion searched argparse help for fixture_mode instead of --fixture-mode
```

Both were assertion-surface defects. Corrections did not weaken runtime acceptance.

## Shadow Architect verdict

```text
LIFECYCLE_DELTA        corrected
AUTHORITY_DELTA        bounded by one-ACTIVE sequential queue
OWNERSHIP_DELTA        exact bundle owner + typed side inputs
RESOURCE_DELTA         inherited runner bounds preserved
FAILURE_SURFACE_DELTA  negative controls exercised
EVIDENCE_DELTA         fixture/live separation + exact subject parity
CONTRACT_DRIFT         canonical skills-shared queue assertion retained
```

No L3 blocker remains for M7 **contract readiness**.

## Residual evidence boundary

```text
real local reviewer execution            NOT_EXERCISED
real live kind/Kubernetes smoke           NOT_EXERCISED
live advanced queue compilation           NOT_EXERCISED
Argo controller runtime                   NOT_EXERCISED
Argo CD Application reconciliation        NOT_EXERCISED
live Rollouts/Prometheus canary            NOT_EXERCISED
llama.cpp/model inference                 NOT_EXERCISED
1,000-VU synthetic execution             NOT_EXERCISED
registry-stored image signing             NOT_EXERCISED
production users/incidents               OUTSIDE_CURRENT_PROOF
people-management tenure                 OUTSIDE_REPOSITORY_PROOF
```

Merge/release/visibility/permissions/production promotion or rollback and real-experience admission remain Human-owned.
