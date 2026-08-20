# M9 — PUBLIC_LOCAL_RECEIPT_ADMISSION_READY

Status: `PASS_BOUNDED`

M9 closes the repository-level gap between **raw typed Local Handoff receipts** and **public GitHub evidence routing**. It adds an exact-subject, fail-closed admission layer that emits a minimal public-safe packet without mutating or advancing the Local Handoff queue.

It does **not** execute any physical/local runtime.

## Exact A9 implementation subject

```text
Issue:          #76
PR:             #77
branch:         feat/m9-local-receipt-admission
base:           main @ 5d0c5db1626bf5c1a83334ea864b6a3eb7613df3
hardened head:  fc7ae40c0a5ea0a403c2ed27555de3cbbc8d042b
tree:           67acc95ed6ee85091dfe30c8b853bc54203c3cda
contract run:   32376416583
result:         SUCCESS
```

Maximum evidence ceiling:

```text
GITHUB_HOSTED_M9_RECEIPT_ADMISSION_CONTRACT_ONLY
```

The exact A9 head will be re-verified if D9 traceability is merged into the A9 branch. Historical run `32376416583` remains evidence only for the head above.

## Real problem

Before M9, local runners could produce durable typed receipts, but the repository lacked one public-safe boundary for bringing those receipts back into GitHub. A naïve workflow could accidentally:

- publish arbitrary raw logs or output tails;
- admit a receipt for the wrong queue subject;
- accept a receipt for an item that is still blocked;
- confuse fixture evidence with live evidence;
- overwrite the queue or raw receipt while writing the public packet;
- expose secret-bearing or oversized local data;
- treat packet compilation as queue advancement.

M9 separates these concerns:

```text
local command
→ raw typed receipt
→ exact-subject admission
→ allowlisted public packet + raw SHA-256/size/path
→ Human/trusted queue review
→ deliberate queue advancement or gap handling
```

## Authoritative admission surface

```text
scripts/handoff/compile_public_receipt_packet.py
  bounded parsing + receipt schema/evidence projection core

scripts/handoff/admit_public_receipt_packet.py
  authoritative live/public admission policy
```

Agents must use the second entrypoint when projecting real local receipts into public GitHub evidence.

## Admission invariants

### Queue authority

The queue must remain canonical `agentic-tech-lead/local-handoff-queue/v1` and must describe one legal frontier:

```text
COMPLETE*
→ exactly one ACTIVE
→ BLOCKED_BY_PREDECESSOR*
```

A receipt assignment must be a contiguous prefix that ends at or before the current ACTIVE item. A receipt for a blocked future item is rejected before any public packet is emitted.

### Receipt identity

Each raw receipt is checked against the current queue for:

```text
schema_version
repository
commit
tree
PASS | FAIL verdict/state
evidence ceiling
required success checks
required cleanup checks
fixture/live evidence kind
```

A completed queue item cannot be represented by a FAIL receipt.

### Public disclosure and resource bounds

The admission layer:

```text
requires explicit receipt roots
rejects filesystem root as a receipt root
limits receipt-root count
limits receipt bytes
rejects path escapes / ambiguous roots
rejects secret-like values and sensitive-key fields
copies only allowlisted summaries
stores raw receipt SHA-256 + byte count + root-relative path
```

It does not copy arbitrary command output or raw log tails by default.

### Mutation authority

For live admission:

```text
public packet output must remain under evidence/local-handoff/
output cannot alias the queue
output cannot alias an input receipt
queue_mutated = false
queue_advanced = false
```

Possible packet routing states are descriptive only:

```text
LOCAL_GAP_OPEN
ACTIVE_RECEIPT_REQUIRED
HUMAN_QUEUE_ADVANCE_REQUIRED
QUEUE_COMPLETION_REVIEW_REQUIRED
```

None is an unattended authority transition.

## Shadow Architect FIRST_GREEN hardening

The first A9 implementation reached CI green, then `MODE=MONITOR` identified additional authority/state gaps.

### `AUTHORITY_DELTA`

Initial compiler output could be pointed at any path inside the repository. That was too broad because a caller could target the queue or a raw receipt. Corrective action:

```text
live output → evidence/local-handoff/** only
+
explicit input-alias rejection
```

### `STATE_DELTA`

Initial compiler validated linear edges but could admit a full receipt prefix even when later items were still `BLOCKED_BY_PREDECESSOR`. Corrective action:

```text
validate COMPLETE* → ACTIVE → BLOCKED* state shape
+
reject receipt for any future blocked item
+
reject FAIL receipt for an already COMPLETE item
```

### `EVIDENCE_DELTA`

The existing secret detector covered common token/key shapes, but the public boundary needed explicit handling for fields such as access/refresh/session tokens, authorization headers and cookies. The hardened wrapper adds those key-level guards and retains fixture/live separation.

### `RESOURCE_DELTA`

Receipt roots are now explicit, bounded in count and cannot be the filesystem root. Raw receipt byte ceilings remain enforced.

No L3 blocker remains for the **M9 contract checkpoint** after run `32376416583`.

## Contract CI evidence

The hardened workflow exercised:

```text
core receipt parser tests                         PASS
Shadow admission-policy tests                    PASS
current ACTIVE receipt fixture admission         PASS
blocked-future receipt negative control          PASS
fixture → live negative control                  PASS
queue-state progression controls                 PASS
output/input authority controls                  PASS
receipt-root bounds                              PASS
extended sensitive-key guard                    PASS
public packet allowlist                          PASS
queue mutation                                   NOT_PERFORMED
physical runtime                                 NOT_EXERCISED
```

## Relationship to current Local Handoff

Current execution subject remains:

```text
commit e7b4e23799a3579572598ebd5864a80831d49db4
tree   0b72b9f09f73d3829db2f138d457a5691641bf79
```

Current queue remains:

```text
M8-LOCAL-REVIEWER-001         ACTIVE
M8-LIVE-KIND-002              BLOCKED_BY_PREDECESSOR
M8-COMPILE-ADVANCED-QUEUE-003 BLOCKED_BY_PREDECESSOR
```

M9 does not replace this queue. It controls how a raw receipt from the current queue is admitted into a public-safe projection before the trusted owner decides whether to advance the queue.

## Git Town / Tech Lead topology

```text
main
└─ A9 PR #77 receipt admission implementation
   └─ D9 issue #78 traceability child
```

D9 is a true child because it consumes unmerged A9 contracts and documents their exact admitted subject. Physical receipts are process dependencies, not Git ancestry.

## Residual evidence boundary

```text
local deterministic reviewer execution       NOT_EXERCISED
live kind/Kubernetes application smoke       NOT_EXERCISED
live advanced queue compilation              NOT_EXERCISED
Argo controller runtime                      NOT_EXERCISED
Argo CD Application reconciliation           NOT_EXERCISED
live Rollouts/Prometheus canary              NOT_EXERCISED
llama.cpp/model inference                    NOT_EXERCISED
1,000-VU synthetic execution                NOT_EXERCISED
registry-stored image signing                NOT_EXERCISED
production users/incidents/tenure            OUTSIDE_CURRENT_PROOF
people-management tenure                    OUTSIDE_REPOSITORY_PROOF
```

Issue #9 remains the physical convergence owner. Merge/release/visibility/permissions, queue advancement, production promotion/rollback, provider credentials and real-experience admission remain Human/trusted-owner operations.
