# M4 — PUBLIC_REMOTE_REVIEWER_CONVERGENCE_FIRST_GREEN

Status: `PASS_BOUNDED`

This milestone records the first hardened public reviewer convergence for issue #9. It combines two orthogonal GitHub-hosted checks on PR #44 without promoting either result beyond its evidence ceiling:

1. **Artifact convergence** re-downloads exact M2/M3 GitHub Actions artifacts, verifies archive SHA-256 identities, admits required public-safe paths, and assembles one bounded reviewer bundle.
2. **Deterministic replay** rebuilds the public Demo Console, replays the bounded backend/failure path, validates current prerequisite PR heads, and preserves all `NOT_EXERCISED` substrate states.

Neither lane proves production runtime, real users, production incidents, or management tenure.

## Exact convergence subject

```text
PR:             #44
branch:         feat/full-reviewer-convergence
base:           feat/failure-recovery-convergence / PR #42
source head:    4ce77c5e0e4ece8379badea5c3fa477a3a463d62
```

### Primary artifact-convergence receipt

```text
workflow:       Full MVP public reviewer convergence
Actions run:    32256405012
artifact:       9366445128
artifact digest sha256:6acd3395bd198e46bd3c31da6a901371a5c2cfaf1552fbc3ee2bf77c53ddfdde
artifact size:  2,841,522 bytes
ceiling:        GITHUB_HOSTED_ARTIFACT_REDOWNLOAD_AND_REVIEWER_BUNDLE_ONLY
```

This run re-downloaded six exact GitHub Actions artifacts for observability, policy/security, ML/LLMOps, Demo Console, supply-chain/fault, and failure/recovery. Each downloaded ZIP was hashed and compared with the recorded GitHub artifact digest before named files were admitted into the reviewer bundle.

### Secondary deterministic-replay receipt

```text
workflow:       Full MVP reviewer convergence
Actions run:    32256405010
artifact:       9366471049
artifact digest sha256:a6b17169bd1fe53122e27b934365fd8add7530e841541ce443637c5265758eef
artifact size:  1,394,199 bytes
ceiling:        GITHUB_HOSTED_REMOTE_REVIEWER_CONVERGENCE_ONLY
```

This run rebuilt the Demo Console, re-ran the seven bounded failure/recovery drills, asserted both business PASS and FAIL Prometheus evidence, validated prerequisite current PR heads, and persisted the residual evidence boundary.

## Observed convergence DAG

```text
M2 remote lane receipts
  PR #36 observability
  PR #38 policy/security
  PR #39 ML/LLMOps
  PR #40 supply-chain/fault
       \
        + PR #42 M3 failure/recovery
        + PR #37 Demo Console
                ↓
        PR #44 X9 reviewer convergence
          ├─ artifact re-download / digest verification
          └─ deterministic replay / current-head readback
                ↓
        M4 PASS_BOUNDED reviewer packet
```

PR #44 has one Git base, PR #42. Demo Console bytes are an explicit exact side input from PR #37; other lane evidence is consumed through exact artifact subjects. Multi-input task convergence does not fabricate multi-parent Git ancestry.

## Reviewer bundle

The primary artifact contains a bounded packet with:

```text
reviewer-bundle/
├── README.md
├── reviewer-index.json
├── reviewer-index.sha256
├── bundle-bytes.txt
├── serve.py
├── console/
└── evidence/
    ├── observability/
    ├── policy-security/
    ├── llmops/
    ├── demo-console/
    ├── supply-chain/
    └── failure-recovery/
```

After downloading that artifact, the local viewing path is deliberately bounded:

```bash
python3 serve.py
```

It serves only the static reviewer console at `127.0.0.1:4173` and performs no production action.

The repository also contains a deterministic developer replay entrypoint:

```bash
bash scripts/demo/run_reviewer_demo.sh reviewer-demo-output
```

That path requires local Python/Node/npm, installs only the demo dependencies, rebuilds the console, replays the bounded incident drills, and emits a local reviewer receipt. It is not a production-runtime proof.

## BEFORE_PUBLIC_DEMO Shadow review

### `EVIDENCE_DELTA` — current PR head versus evidence head

Failure/recovery PR #42 advanced after its successful evidence run through a temporary no-op marker and revert. Therefore the current PR head and the artifact evidence head are not the same subject.

The hardened convergence keeps them separate:

```text
PR #42 current head:   c7e6a30af5b70bff6a7ac78eab2eb4bd0d46724e
M3 evidence head:      e48711055572d83c872e72445cdf1389592ce85e
M3 evidence artifact:  9365550423
```

A newer PR head does not silently re-label an older artifact as evidence for the newer head.

### `EVIDENCE_DELTA` — artifact existence versus artifact readback

M2/M3 previously bound artifact IDs/digests. M4 primary convergence upgrades this by re-downloading the six exact artifacts and verifying the downloaded archive SHA-256 values before admission.

This closes the earlier `SIDE_INPUT_ARTIFACT_REDOWNLOAD_NOT_EXERCISED` gap **for the six M4 input artifacts only**. It does not prove registry-stored image signatures, production deployment artifacts, or future artifact availability after retention expiry.

### `OWNERSHIP_DELTA` — duplicate convergence surfaces

Two convergence workflows exist on PR #44. They are retained only because their evidence obligations are different:

```text
full-reviewer-convergence.yml
→ prior-artifact re-download + digest verification + static reviewer bundle

full-reviewer-demo.yml
→ deterministic fresh replay + current PR-head readback + console rebuild
```

Neither workflow may promote the other's ceiling. If later maintenance makes the obligations identical, they should be collapsed into one owner rather than allowed to drift.

### `RESOURCE_DELTA`

The reviewer bundle is explicitly capped below 5 MB and the observed primary artifact is 2,841,522 bytes. Public secret-pattern checks run before persistence.

## What M4 actually proves

```text
exact M2/M3 artifact re-download                     PASS
artifact archive SHA-256 verification                PASS
required public evidence path admission              PASS
bounded static reviewer bundle                       PASS
Demo Console public evidence rendering               PASS
seven DRILL failure/recovery records preserved       PASS
deterministic failure/recovery replay                PASS
business PASS + FAIL telemetry in replay             PASS
current prerequisite PR-head readback                PASS
no paid model/provider API required                  PASS
```

## Residual proof boundary

```text
live kind/Kubernetes deployment                      NOT_EXERCISED
real Argo CD reconciliation                           NOT_EXERCISED
live Argo Rollouts + Prometheus canary               NOT_EXERCISED
local Qwen / llama.cpp runtime                       NOT_EXERCISED
1,000-VU capacity and recovery                       NOT_EXERCISED
registry-stored image signing                        NOT_EXERCISED
production user/adoption evidence                    OUTSIDE_REPOSITORY_PROOF
production incident history                          NOT_EXERCISED
real people-management tenure                        OUTSIDE_REPOSITORY_PROOF
merge/release/visibility/production authority        HUMAN_ONLY
```

`M4 PASS_BOUNDED` is therefore **reviewer-demo-ready at the remote public evidence ceiling**, not production-ready.

## Next legal frontier

```text
M4 public reviewer packet
        +
Local Handoff receipts for live kind/model/Argo paths when available
        ↓
optional higher-substrate evidence admission
        +
Product-Manager-Notes interview/evidence convergence
```

The public MVP now has a recruiter/reviewer path even before those local-substrate residuals are admitted, but every missing runtime layer must remain visibly `NOT_EXERCISED`.
