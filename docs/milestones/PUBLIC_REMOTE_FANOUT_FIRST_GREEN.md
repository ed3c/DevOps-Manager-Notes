# M2 — PUBLIC_REMOTE_FANOUT_FIRST_GREEN

Status: `PASS_BOUNDED`

This milestone records the first independently observed GitHub-hosted execution receipts for the five public fan-out lanes that start from Core FIRST_GREEN source `a4ce65dbd66b32bdd2d313f03f8ac97b6bf01f10` (PR #14).

`PASS_BOUNDED` is not full runtime closure. It does not prove live kind/Kubernetes, real Argo reconciliation, a local model/llama.cpp run, a 1,000-VU run, production traffic/adoption, production incident history, or employment/management tenure.

## Observed molecular stack

```text
PR #13  E1 invariant/evidence freeze
   ↓ true child
PR #14  K2 Core remote FIRST_GREEN
   ├─ PR #36  A3  #3  observability / SLI-SLO / bounded load
   ├─ PR #38  E4  #4  policy / security / license metadata
   ├─ PR #39  A7  #7  ML/LLMOps / progressive-delivery contract
   ├─ PR #37  A8  #8  recruiter-facing Demo Console
   └─ PR #40  E10 #10 supply-chain / bounded fault drill
          │
          └──── exact admitted side-input receipts ────┐
                                                       ▼
                                                #5 X5 failure/recovery
                                                       │
                                                + #8 UI receipt
                                                       ▼
                                                #9 X9 final demo
```

The five fan-out branches are siblings because they start from the same frozen Core subject and do not consume each other's unmerged bytes. #3 has an observed path-lease delta because request telemetry required the smallest shared Core app integration. No other sibling consumed that mutation.

## Exact remote FIRST_GREEN subjects

| Lane | PR | Source head | Actions run | Artifact | Artifact digest | Evidence ceiling |
|---|---:|---|---:|---:|---|---|
| #3 Observability/load | #36 | `f52763b8b6df6c3ed5d9fc4117412e06129f2f17` | `32249524958` | `9363866816` | `sha256:de464ff881638a42f9bf536ff7ba6e255d1e419647ce1522002fdbaac4201430` | `GITHUB_HOSTED_OBSERVABILITY_AND_SYNTHETIC_LOAD_SMOKE_ONLY` |
| #4 Policy/security | #38 | `b0c9db1ed691ca8c32770ad666ca6708c6294c1f` | `32251169964` | `9364485321` | `sha256:68ac7b4ce0b7bfc2535c54b1960d3b56152fd4947bf031c56c00eb5f7f5f7b4b` | `GITHUB_HOSTED_POLICY_SECURITY_AND_LICENSE_METADATA_ONLY_NOT_LEGAL_CLEARANCE` |
| #7 ML/LLMOps | #39 | `f8141534541b0e87f3065e5dd9d60f459539a3ba` | `32250421421` | `9364219603` | `sha256:ba3a173b4d64935449836b09881d7e490cf3873de7218af66b293bc17c5d4e27` | `GITHUB_HOSTED_DETERMINISTIC_MLFLOW_LIFECYCLE_ONLY` |
| #8 Demo Console | #37 | `1081f471710158a5e76cc0e373504cbcd0a27940` | `32251120563` | `9364438271` | `sha256:544a3c968918814c03e24144b373393735a5e25f6825052d26e08b45ff284a0a` | `FRONTEND_BUILD_AND_CANONICAL_PUBLIC_EVIDENCE_RENDER_ONLY` |
| #10 Supply/fault | #40 | `b03133142c987125eacf173131311bf12de370ed` | `32251234101` | `9364488819` | `sha256:74b1664bdd836d4bf94cf4e089e5549d6917dd48aafef0b5e6d82bf6df493eda` | `GITHUB_HOSTED_SBOM_SAME_RUN_BLOB_SIGNING_AND_BOUNDED_FAULT_DRILL_ONLY` |

## What each lane actually proved

### #3 Observability / SLO / bounded load

Exercised request trace identity, Prometheus metrics, business-oracle metrics, SLI/SLO contract and a bounded `20 VU / 5 s` Locust smoke. The negative control keeps liveness/transport healthy while the business oracle reports failure.

`1,000 VU`, production traffic and real adoption remain `NOT_EXERCISED`.

### #4 Policy / security / license metadata

Exercised positive/negative OPA deployment admission, an installed-Python license metadata inventory with a planted forbidden-license negative control, and a Trivy CRITICAL vulnerability gate. OPA and Trivy image subjects are digest-pinned after the first observed run.

This is not blanket legal/commercial/transitive clearance.

### #7 ML/LLMOps

Exercised an explicit model/prompt/config/dataset lifecycle, an MLflow tracking run, offline evaluation admission, a planted `offline PASS → canary business FAIL` case, and deterministic rollback to the declared previous-good revision.

The Qwen artifact remains unmaterialized; exact model revision/file/digest, llama.cpp runtime and live Argo Rollouts/Prometheus canary remain `NOT_EXERCISED`.

### #8 Demo Console

Exercised the React/Vite/TanStack Query/ECharts public build that compiles its state from canonical evidence/gap registries, plus public secret-pattern and build-size checks. After Shadow review, source maps were removed and the persisted artifact fell from roughly 8.47 MB to 1,358,050 bytes; setup-node is pinned to the exact subject observed during the first run.

The UI has zero authority to promote backend/runtime evidence.

### #10 Supply-chain / fault drill

Exercised checksum-verified Syft installation, an exact Core image archive identity, CycloneDX SBOM, Cosign same-run blob signature/verification, planted tampered-blob rejection, and a digest-pinned Toxiproxy 450 ms latency injection with cleanup verification.

After Shadow resource review, the heavyweight image archive is removed before evidence upload; the hardened persisted packet is 1,057,880 bytes. Later independent blob re-verification, registry-stored image signing and production incident behavior remain `NOT_EXERCISED`.

## Shadow Architect delta ledger

| Delta | Observation | Required invariant / response |
|---|---|---|
| `OWNERSHIP_DELTA` | #3 needed two minimal shared Core app mutations to wire telemetry | no sibling may consume/overwrite those unmerged bytes; convergence must reconcile exact subjects |
| `RESOURCE_DELTA` | #8 first build persisted source maps and was ~8.47 MB | disable public source maps; persist a bounded build and exact npm-tree digest |
| `SUPPLY_CHAIN_DELTA` | #8 initially used a moving `setup-node@v6` ref | pin exact action SHA observed at first run |
| `SUPPLY_CHAIN_DELTA` | #4 initially used OPA/Trivy image tags | pin exact observed image digests before hardened FIRST_GREEN |
| `RESOURCE_DELTA` | #10 first artifact persisted a ~191 MB Docker archive | remove heavyweight archive before persistence; explicitly lower later-reverification claim ceiling |
| `SUPPLY_CHAIN_DELTA` | #10 initially used a Toxiproxy tag | pin exact observed image digest |
| `AUTHORITY_DELTA` / `EVIDENCE_DELTA` | GitHub metadata reports Product and DevOps repositories public; Product docs had called Product private | documentation/disclosure contract must follow observed visibility; never mutate visibility automatically |

No L3 block remains for the **remote M2 lane checkpoint**. L1/L2 residuals below still prevent full runtime/failure closure.

## Residual proof obligations

```text
live kind/Kubernetes deployment               NOT_EXERCISED
real Argo CD reconciliation                    NOT_EXERCISED
1,000-VU capacity run                          NOT_EXERCISED
local Qwen artifact revision/file/digest       NOT_EXERCISED
llama.cpp model runtime                        NOT_EXERCISED
live Argo Rollouts + Prometheus canary          NOT_EXERCISED
later independent signed-blob re-verification  NOT_EXERCISED
registry-stored image signing                  NOT_EXERCISED
#5 cross-lane failure/recovery convergence      NOT_IMPLEMENTED
#9 one-command reviewer convergence            NOT_IMPLEMENTED
real production users/incidents/tenure         OUTSIDE_REPOSITORY_PROOF
```

## Next legal frontier

Remote public fan-out is complete at its declared ceiling. The next Tech Lead frontier is:

```text
Local Handoff receipts where the exact substrate is required
        +
#5 failure/recovery convergence
        ↓
seeded failure
→ detection
→ incident decision
→ mitigation / rollback / recovery
→ postmortem
→ corrective change
→ same-failure re-test
        ↓
#9 final reviewer convergence
```

Do not close underlying issues #3/#4/#7/#8/#10 merely because this remote milestone is green; each remains open until its full issue acceptance/evidence ceiling is satisfied or explicitly re-scoped.
