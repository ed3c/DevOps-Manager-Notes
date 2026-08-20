# Public Reviewer Convergence

Issue #9 is the sole owner of the final **public remote reviewer convergence** under `scripts/demo/`. This surface does not merge or publish production state; it re-downloads exact GitHub Actions artifacts, verifies their SHA-256 identities, admits only required public-safe files, and assembles one bounded reviewer packet.

## State machine

```text
EXACT_INPUT_MANIFEST_BOUND
→ ARTIFACTS_REDOWNLOADING
→ ARTIFACT_DIGESTS_VERIFIED
→ REQUIRED_PATHS_ADMITTED
→ REVIEWER_PACKET_ASSEMBLED
→ PUBLIC_BOUNDARY_CHECKED
→ REVIEWER_PACKET_PERSISTED
→ REMOTE_REVIEWER_FIRST_GREEN

missing/expired/mismatched artifact
→ CONVERGENCE_BLOCKED
```

`REMOTE_REVIEWER_FIRST_GREEN` does not imply live Kubernetes, Argo, local model execution, 1,000-VU recovery, production users/incidents, or management tenure.

## Remote one-command equivalent

The canonical CI entrypoint is the `Full MVP public reviewer convergence` workflow. It needs only the repository-scoped GitHub Actions token supplied by GitHub; no paid model/provider API key is required.

The resulting artifact contains:

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

After downloading the bounded reviewer artifact, local viewing is one command:

```bash
python3 serve.py
```

This serves the static console on `http://127.0.0.1:4173/` and performs no external side effects.

## Evidence rules

- Artifact identity is verified against `evidence/receipts/convergence/public-m4-inputs.json`.
- The bundle copies only named evidence files plus the already-built public console.
- UI state cannot promote backend/runtime evidence.
- `DRILL` remains `DRILL`; virtual users remain synthetic load evidence.
- Missing local/substrate evidence remains `NOT_EXERCISED`.
- Merge, release, repository visibility/permissions, production actions, and real-experience admission remain Human-owned.
