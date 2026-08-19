# Delivery and Incident Metrics

These metrics are decision inputs for the demo system; they are not claims about a historical employer or production organization.

## Required measures

| Measure | Decision use | Failure mode it prevents |
|---|---|---|
| change failure rate | decide whether rollout policy is too permissive | optimizing deployment frequency while regressions rise |
| mean detection time | evaluate detector coverage | green infrastructure masking business failure |
| mean recovery time | compare rollback/repair strategies | slow diagnosis without a bounded recovery path |
| rollback success rate | verify previous-good assumptions | declaring rollback readiness without exercise |
| same-failure re-test pass rate | prove corrective action | postmortem without preventive closure |
| queue saturation events | capacity/backpressure decisions | unbounded memory/latency growth |
| authorization denials by capability | identify missing/over-broad authority | privilege widening as incident response |
| drill evidence completeness | enforce receipt closure | prose-only incident claims |

## Decision law

A metric must name its subject, window/profile, and evidence lane. Synthetic drill values never become production SLO history. If a metric is missing, the corresponding decision remains bounded or `NOT_EXERCISED`.

## Closure gate

A failure drill is considered closed only when:

```text
detection PASS
AND recovery PASS
AND corrective change recorded
AND same-failure re-test PASS
AND exact receipt persisted
```
