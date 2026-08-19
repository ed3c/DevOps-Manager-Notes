# M4 — PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN

Status: `PASS_BOUNDED`

This milestone records the hardened public reviewer convergence for issue #9. It combines the admitted M2 lane receipts, the M3 failure/recovery receipt, and the exact Demo Console byte input into bounded reviewer artifacts without promoting any local/substrate or production claim.

## Exact execution subject

```text
PR:               #44
branch:           feat/full-reviewer-convergence
Git parent:       PR #42 / feat/failure-recovery-convergence
source head:      55d18cdc556ca5d66c67406318ae25196c077fd2
source tree:      a4ad37d9baf73a5239f79c516c67b0182420336a
Demo Console:     PR #37 evidence head 1081f471710158a5e76cc0e373504cbcd0a27940
```

PR #44 remains draft/open. Merge, release and publication admission remain Human-owned.

## Hardened remote receipts

### Deterministic one-command reviewer lane

```text
workflow:         Full MVP reviewer convergence
run:              32256802856
artifact:         9366615717
artifact digest:  sha256:e652cdf3ccb8de7a8655f9148bc6471a29bcaeaef2d55f6255bca2cb2b1e19d3
artifact size:    1,394,198 bytes
verdict:          PASS_BOUNDED
evidence ceiling: GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY
```

Exercised:

```text
exact Demo Console byte parity against PR #37 evidence head
current prerequisite PR-head readback
current-head vs historical-evidence-head separation
Python/Node bounded deterministic reviewer bootstrap
Demo Console typecheck/build/public evidence guard
seven DRILL failure/recovery scenarios
complete incident timelines
business PASS + FAIL Prometheus visibility
same-failure re-test
no paid model/provider API dependency
```

The repository entrypoint is:

```bash
bash scripts/demo/run_reviewer_demo.sh <output-directory>
```

### Exact Actions artifact re-download lane

```text
workflow:         Full MVP public reviewer convergence
run:              32256802554
artifact:         9366596481
artifact digest:  sha256:696f56be2fb637e386941eb313caa7c9448900ad0bad88b3a96119b95315596c
artifact size:    2,841,522 bytes
verdict:          PASS_BOUNDED
evidence ceiling: GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY
```

This lane independently re-downloaded and verified the published GitHub Actions artifact archive digests for:

```text
#36 observability / load
#38 policy / security / license
#39 ML / LLMOps
#37 Demo Console
#40 supply chain / bounded fault
#42 failure / recovery
```

Only named public-safe paths were admitted into the bundle. The persisted packet contains a static evidence console, exact lane evidence, reviewer index, explicit residual gaps and a local static viewer.

## #9 state machine

```text
M2_RECEIPTS_BOUND
+ M3_FAILURE_RECEIPT_BOUND
+ DEMO_CONSOLE_BYTE_SUBJECT_BOUND
→ PR_CURRENT_HEADS_READ_BACK
→ ARTIFACT_EVIDENCE_HEADS_SEPARATED
→ DEMO_CONSOLE_BYTES_VERIFIED
→ ACTIONS_ARTIFACTS_REDOWNLOADED
→ ARTIFACT_DIGESTS_VERIFIED
→ REQUIRED_PATHS_ADMITTED
→ DETERMINISTIC_REVIEWER_PATH_EXECUTED
→ FAILURE_DRILLS_REVERIFIED
→ PUBLIC_BOUNDARY_CHECKED
→ REVIEWER_PACKET_PERSISTED
→ REMOTE_REVIEWER_FIRST_GREEN

stale current head / digest mismatch / byte mismatch /
missing required path / secret-like public material
→ CONVERGENCE_BLOCKED
```

## Observed molecular Stack

```text
PR #14 Core
├─ PR #36 Observability
├─ PR #38 Policy/Security
├─ PR #39 ML/LLMOps
├─ PR #37 Demo Console
└─ PR #40 Supply/Fault

PR #36
└─ PR #42 Failure/Recovery          TRUE_CHILD + CONVERGENCE
     ↑ exact evidence identities #38/#39/#40

PR #42
└─ PR #44 Reviewer Convergence      TRUE_CHILD + CONVERGENCE
     ↑ exact Demo Console bytes #37
     ↑ exact M2/M3 Actions artifacts
     └─ PR #45 Local Handoff Queue  TRUE_CHILD / LOCAL_HANDOFF
```

PR #44 has one Git parent, PR #42. Other task prerequisites are explicit byte/evidence side inputs rather than fabricated Git parents.

## Shadow Architect hardening

### `EVIDENCE_DELTA` — mutable PR head vs historical evidence subject

An earlier #9 workflow correctly failed because PR #42 had advanced through no-net-diff marker/revert commits after the successful M3 evidence run. Comparing a mutable current PR head directly to a historical evidence head would either block valid routing or encourage evidence laundering.

The contract now separates:

```text
current_head  = current mutable PR routing subject
evidence_head = exact commit that produced the admitted artifact
```

For PR #42:

```text
current PR head: c7e6a30af5b70bff6a7ac78eab2eb4bd0d46724e
M3 evidence head: e48711055572d83c872e72445cdf1389592ce85e
M3 artifact:      9365550423
```

A newer PR head never relabels an older artifact as evidence for the newer head.

### `DAG / EVIDENCE_DELTA` — Demo Console byte consumption

#9 consumes Demo Console bytes, not merely a claim that #37 exists. The hardened workflow fetches the exact PR #37 evidence head and requires:

```text
git diff --exit-code 1081f471710158a5e76cc0e373504cbcd0a27940 -- demo-console
```

before convergence can pass.

### `EVIDENCE_DELTA` — artifact readback

M3 left `side_input_artifact_redownload` as `NOT_EXERCISED`. M4 closes that specific gap for the six bound M2/M3 Actions artifacts by downloading each archive again and checking its SHA-256 digest before admitting required paths.

This does not prove future artifact availability after retention expiry, registry-stored image signatures, or production deployment artifacts.

### `OWNERSHIP_DELTA` — two convergence workflows

Two #9 workflows are retained because their proof obligations remain different:

```text
full-reviewer-convergence.yml
→ prior-artifact re-download + digest verification + bounded static packet

full-reviewer-demo.yml
→ fresh deterministic replay + current-head readback + exact Demo Console byte parity
```

If those obligations later become identical, one owner should replace both rather than allowing drift.

### `RESOURCE_DELTA`

Both persisted reviewer artifacts remain below the 5 MB public evidence budget:

```text
one-command reviewer artifact: 1,394,198 bytes
artifact-reverified bundle:     2,841,522 bytes
```

No L3 blocker remains for the **remote reviewer convergence checkpoint**.

## Local Handoff boundary

PR #45 binds the hardened M4 source into the Tech Lead Local Handoff Execution Queue.

ACTIVE local reviewer command:

```bash
bash scripts/demo/run_reviewer_demo.sh evidence/local-reviewer
```

Receipt:

```text
evidence/local-reviewer/reviewer-demo-receipt.json
```

Evidence ceiling:

```text
LOCAL_DETERMINISTIC_REVIEWER_RUN_ONLY
```

The next live-substrate item remains `BLOCKED_UNRESOLVED` until concrete committed runners, exact artifacts, budgets and cleanup contracts exist. No speculative kind/Argo/model/1,000-VU command is presented as executed evidence.

## Residual proof obligations

```text
live kind/Kubernetes                         NOT_EXERCISED
real Argo CD reconciliation                  NOT_EXERCISED
live Argo Rollouts + Prometheus canary       NOT_EXERCISED
local Qwen / llama.cpp inference             NOT_EXERCISED
1,000-VU capacity and recovery               NOT_EXERCISED
registry-stored image signature              NOT_EXERCISED
production users / adoption                  OUTSIDE_REPOSITORY_PROOF
production incident history                  OUTSIDE_REPOSITORY_PROOF
real people-management tenure                OUTSIDE_REPOSITORY_PROOF
```

`M4 PASS_BOUNDED` means **reviewer-demo-ready at the remote public evidence ceiling**, not production-ready.

## Stage boundary

Remote #9 reviewer convergence is stage-complete at its declared ceiling. The next engineering frontier is the typed Local Handoff/live-substrate program plus Product-side interview/public-portfolio projection from exact admitted M4 subjects.

Merge, release, repository visibility/permission changes, production promotion/rollback and real-experience claims remain Human-owned.
