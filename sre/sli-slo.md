# Full Manager MVP — SLI / SLO Contract

## Evidence boundary

This is a demo/runtime contract. Synthetic load is not real user adoption and GitHub-hosted load is not production traffic.

## Workload identity

Every reported result names: source commit, environment, request mix, virtual users, spawn rate, duration, percentile window and receipt path.

## SLIs

- Availability SLI: successful business-eligible requests / admitted requests. Transport `2xx` alone is insufficient when the business oracle fails.
- Latency SLI: `manager_demo_http_request_duration_seconds`, report p50/p95/p99.
- Error SLI: HTTP 5xx plus business-oracle FAIL as separate dimensions.
- Saturation signals: in-flight requests, CPU/memory where the substrate exposes them, DB pool/connection pressure and load-generator no-progress.

## Demo SLO

For the bounded smoke profile only:

```text
window: one declared test run
p95 request latency: <= 500 ms without injected fault
transport error rate: < 1%
business-oracle mismatch: 0 for happy-path workload
```

A run that cannot report its workload/environment is `ABSENT`, not PASS.

## Error budget

For a run of N admitted requests, the transport error budget is `floor(N * 0.01)`. Business-oracle failures are not hidden inside that budget; seeded failures are recorded as negative-control evidence.

## 1,000 VU rule

`tests/load/locustfile.py` supports a 1,000-virtual-user profile, but `1000_VU = NOT_EXERCISED` until an exact run receipt names the environment and succeeds. Even then, the claim ceiling is synthetic capacity evidence only.
