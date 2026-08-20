# M9 receipt-admission fixtures

These JSON files are explicit `evidence_kind=FIXTURE` inputs for the M9 compiler contract.

They are not Local Handoff receipts, do not satisfy any live predecessor edge, and must be rejected unless `--fixture-mode` is supplied.

The fixture payloads deliberately contain raw log-tail markers so CI can prove the public packet compiler omits non-allowlisted output.
