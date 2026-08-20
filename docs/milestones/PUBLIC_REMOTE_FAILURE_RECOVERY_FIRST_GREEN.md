# M3 — PUBLIC_REMOTE_FAILURE_RECOVERY_FIRST_GREEN

Status: `PASS_BOUNDED`

This milestone records the first hardened GitHub-hosted failure/recovery convergence for issue #5. It is a **DRILL/SIMULATION** milestone, not production incident history.

## Exact execution subject

```text
PR:             #42
branch:         feat/failure-recovery-convergence
base:           feat/observability-slo-load / PR #36
source head:    e48711055572d83c872e72445cdf1389592ce85e
Actions run:    32254018953
artifact:       9365550423
artifact digest sha256:098ba3e3427323c9c4651d5d8683d174723039d5fe32285045f95773d7419558
artifact size:  25,773 bytes
```

Evidence ceiling:

```text
GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY
```

The PR is a true child of PR #36 because the drill executes against the unmerged telemetry-enabled Core app. Other prerequisite lanes are consumed only as exact side-input identities:

```text
#4  policy/security/license     PR #38
#7  ML/LLMOps lifecycle        PR #39
#10 supply-chain/fault         PR #40
```

The Demo Console (#8 / PR #37) is intentionally **not** a #5 dependency; it remains a separate input to #9 final reviewer convergence.

## Seven exercised drills

| ID | Drill | Main detector / recovery proof | Lane |
|---|---|---|---|
| FR-01 | bad release / application regression | business oracle fails while HTTP liveness stays green; previous-good behavior is re-admitted | L3 |
| FR-02 | dependency slowdown / timeout | 50 ms budget rejects injected 250 ms wait; bounded recovery and same-failure timeout re-test | L3 |
| FR-03 | queue pressure | bounded queue raises saturation/no-progress signal; backpressure/drain restores progress | L2 |
| FR-04 | duplicate-side-effect hazard | idempotency identity prevents a second durable effect and rejects conflicting replay | L2 |
| FR-05 | credential / permission failure | missing `deploy:write` fails closed; minimal scope restores the bounded action | L2 |
| FR-06 | observability blind spot | infrastructure live + business fail is explicitly detected and re-tested | L3 |
| FR-07 | restore / DR assumption failure | checksum detects corruption; known-good backup restore is verified twice | L3 |

Every drill records:

```text
trigger
→ detection
→ incident authority
→ mitigation
→ recovery
→ postmortem
→ corrective change
→ same-failure re-test
→ receipt
```

The workflow also proves the Prometheus surface contains both PASS and FAIL business-oracle outcomes while the service remains live.

## Manager artifacts added by #42

```text
incidents/README.md
runbooks/failure-recovery.md
management/ownership-model.md
management/oncall-model.md
management/delegation.md
management/delivery-metrics.md
tests/failure/scenarios/run_failure_drills.py
tests/failure/scenarios/test_failure_primitives.py
evidence/receipts/failure/public-m2-side-inputs.json
.github/workflows/failure-recovery.yml
```

These files demonstrate a public-safe incident-command and delegation model. They do not prove historical direct-report management or production on-call tenure.

## FIRST_GREEN Shadow review

The first successful run triggered a second Shadow review rather than immediate closure.

### `EVIDENCE_DELTA`

The first workflow summary used an unquoted heredoc containing Markdown backticks. Bash interpreted the backtick contents as commands. The job still returned green, so relying only on job status would have hidden a summary-surface defect.

Corrective change:

```text
unquoted heredoc → quoted heredoc
```

The hardened run has no command-substitution warnings.

### `DAG_DELTA`

The first side-input manifest incorrectly included #8 Demo Console even though #5 does not consume UI evidence. That would have created a false completion edge.

Corrective change:

```text
#5 side inputs: #3/#4/#7/#10
#8 remains exclusively a #9 convergence input
```

### `SUPPLY_CHAIN / EVIDENCE_DELTA`

The hardened run persists a sorted `pip freeze` environment and its SHA-256 identity. It also explicitly labels side-input artifact re-download as `NOT_EXERCISED`; the workflow validates the bound manifest shape but does not pretend to have re-fetched every sibling artifact.

### `EVIDENCE_DELTA`

CI now rejects a drill report unless all seven scenarios are `DRILL`, all are PASS, and all required timeline fields are non-empty.

## Closure boundary

This milestone proves bounded incident-process mechanics and same-failure re-verification. It does **not** prove:

```text
production incident history                    NOT_EXERCISED
production Kubernetes recovery                 NOT_EXERCISED
real customer/user impact                      NOT_EXERCISED
real Argo CD / Rollouts recovery               NOT_EXERCISED
local Qwen / llama.cpp recovery                NOT_EXERCISED
1,000-VU recovery behavior                     NOT_EXERCISED
real people-management tenure                  OUTSIDE_REPOSITORY_PROOF
```

No L3 Shadow block remains for the **remote #5 drill checkpoint**.

## Next legal frontier

```text
M2 public remote fan-out receipts
              +
M3 #5 failure/recovery receipt
              +
#8 Demo Console receipt
              ↓
#9 one-command reviewer convergence
              ↓
Local Handoff receipts for live kind/model/Argo paths where required
```

#9 must preserve the evidence ladder and may not turn remote/local drills into production experience. Merge, release, visibility/permission changes, production promotion/rollback and real-experience claims remain Human-owned.
