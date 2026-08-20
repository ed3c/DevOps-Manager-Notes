#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import queue
import shutil
import socket
import sqlite3
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import error, request


def _json_request(url: str, payload: dict | None = None, timeout: float = 2.0) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data else "GET",
    )
    with request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        return json.loads(body.decode("utf-8")) if body else {"status": response.status}


def _subject(source_commit: str, profile: str) -> dict:
    return {
        "git_commit": source_commit,
        "workload_or_fault_profile": profile,
    }


def _result(
    *,
    scenario_id: str,
    title: str,
    lane: str,
    role: str,
    trigger: str,
    detection: str,
    mitigation: str,
    recovery: str,
    postmortem: str,
    corrective_change: str,
    retest: str,
    verdict: str,
    observations: dict,
) -> dict:
    return {
        "scenario_id": scenario_id,
        "title": title,
        "classification": "DRILL",
        "evidence_lane": lane,
        "incident_authority": {
            "incident_commander": "may stop the bounded demo rollout and order rollback/recovery",
            "executor_role": role,
            "human_only": [
                "production promotion",
                "production rollback admission",
                "real customer/user impact claims",
            ],
        },
        "timeline": {
            "trigger": trigger,
            "detection": detection,
            "mitigation": mitigation,
            "recovery": recovery,
            "postmortem": postmortem,
            "corrective_change": corrective_change,
            "same_failure_retest": retest,
        },
        "observations": observations,
        "verdict": verdict,
        "evidence_ceiling": "GITHUB_HOSTED_FAILURE_DRILL_ONLY_NOT_PRODUCTION_INCIDENT_HISTORY",
    }


def exercise_bad_release(base_url: str, source_commit: str) -> dict:
    live = _json_request(f"{base_url}/health/live")
    bad = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "bad-release"),
            "expected_value": "stable-answer",
            "observed_value": "regressed-answer",
            "force_failure": False,
        },
    )
    recovered = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "bad-release-recovery"),
            "expected_value": "stable-answer",
            "observed_value": "stable-answer",
            "force_failure": False,
        },
    )
    retest = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "bad-release-retest"),
            "expected_value": "stable-answer",
            "observed_value": "regressed-answer",
            "force_failure": False,
        },
    )
    ok = (
        live.get("status") == "alive"
        and bad.get("infrastructure_http_ok") is True
        and bad.get("business_ok") is False
        and bad.get("evidence", {}).get("verdict") == "FAIL"
        and recovered.get("business_ok") is True
        and retest.get("business_ok") is False
    )
    return _result(
        scenario_id="FR-01",
        title="Bad release / application regression",
        lane="L3",
        role="release-operator",
        trigger="serve a candidate whose observed business value differs from the expected value",
        detection="business oracle fails while HTTP liveness remains healthy",
        mitigation="stop promotion and select the declared previous-good behavior",
        recovery="expected and observed business values match again",
        postmortem="transport health alone was insufficient to admit the candidate",
        corrective_change="promotion gate requires an explicit business-oracle PASS",
        retest="re-inject the same mismatch and require the oracle to reject it again",
        verdict="PASS" if ok else "FAIL",
        observations={
            "liveness": live,
            "bad_release": bad,
            "recovered": recovered,
            "same_failure_retest": retest,
        },
    )


class _DelayedHandler(BaseHTTPRequestHandler):
    delay_seconds = 0.25

    def do_GET(self) -> None:
        time.sleep(type(self).delay_seconds)
        body = b'{"status":"dependency-ok"}\n'
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *_args) -> None:
        return


def _dependency_request(url: str, timeout: float) -> bool:
    try:
        with request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except (TimeoutError, socket.timeout, error.URLError):
        return False


def exercise_dependency_timeout() -> dict:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _DelayedHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/dependency"
    try:
        _DelayedHandler.delay_seconds = 0.25
        timed_out = not _dependency_request(url, timeout=0.05)
        _DelayedHandler.delay_seconds = 0.0
        recovered = _dependency_request(url, timeout=0.5)
        _DelayedHandler.delay_seconds = 0.25
        retest = not _dependency_request(url, timeout=0.05)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1.0)

    ok = timed_out and recovered and retest
    return _result(
        scenario_id="FR-02",
        title="Dependency slowdown / timeout",
        lane="L3",
        role="service-owner",
        trigger="inject a bounded 250 ms dependency delay",
        detection="a 50 ms client budget expires instead of waiting without bound",
        mitigation="fail fast and route the bounded drill to the healthy dependency behavior",
        recovery="the dependency responds within the allowed budget",
        postmortem="unbounded dependency waits amplify incidents and consume worker capacity",
        corrective_change="every external call owns an explicit timeout budget and bounded fallback",
        retest="restore the 250 ms delay and require timeout detection again",
        verdict="PASS" if ok else "FAIL",
        observations={
            "timeout_detected": timed_out,
            "recovery_probe": recovered,
            "same_failure_retest": retest,
            "timeout_budget_ms": 50,
            "injected_delay_ms": 250,
        },
    )


def exercise_queue_pressure() -> dict:
    work = queue.Queue(maxsize=2)
    work.put_nowait("a")
    work.put_nowait("b")
    try:
        work.put_nowait("overflow")
        detected = False
    except queue.Full:
        detected = True

    drained = work.get_nowait()
    work.task_done()
    work.put_nowait("c")
    recovered = work.qsize() == 2 and drained == "a"

    retest_queue = queue.Queue(maxsize=1)
    retest_queue.put_nowait("a")
    try:
        retest_queue.put_nowait("b")
        retest = False
    except queue.Full:
        retest = True

    ok = detected and recovered and retest
    return _result(
        scenario_id="FR-03",
        title="Resource saturation / queue pressure",
        lane="L2",
        role="capacity-owner",
        trigger="fill a bounded queue to capacity and attempt one extra enqueue",
        detection="the no-progress oracle reports queue.Full instead of silently growing memory",
        mitigation="apply backpressure and drain one unit of work",
        recovery="bounded enqueue resumes after capacity is available",
        postmortem="unbounded queues hide overload until latency or memory fails catastrophically",
        corrective_change="queue capacity and saturation behavior are explicit contract values",
        retest="fill a fresh bounded queue and require overflow detection again",
        verdict="PASS" if ok else "FAIL",
        observations={
            "overflow_detected": detected,
            "recovered_queue_size": work.qsize(),
            "same_failure_retest": retest,
        },
    )


def exercise_duplicate_side_effect() -> dict:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE effects (idempotency_key TEXT PRIMARY KEY, payload_hash TEXT NOT NULL)"
    )

    def apply(key: str, payload: str) -> str:
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        row = conn.execute(
            "SELECT payload_hash FROM effects WHERE idempotency_key = ?", (key,)
        ).fetchone()
        if row:
            return "REPLAY" if row[0] == digest else "CONFLICT"
        conn.execute(
            "INSERT INTO effects(idempotency_key, payload_hash) VALUES (?, ?)",
            (key, digest),
        )
        conn.commit()
        return "APPLIED"

    first = apply("incident-key-001", "charge:100")
    replay = apply("incident-key-001", "charge:100")
    conflict = apply("incident-key-001", "charge:999")
    count = conn.execute("SELECT COUNT(*) FROM effects").fetchone()[0]
    retest = apply("incident-key-001", "charge:100")
    conn.close()

    ok = (
        first == "APPLIED"
        and replay == "REPLAY"
        and conflict == "CONFLICT"
        and count == 1
        and retest == "REPLAY"
    )
    return _result(
        scenario_id="FR-04",
        title="Retry / duplicate-side-effect hazard",
        lane="L2",
        role="data-integrity-owner",
        trigger="repeat the same side-effect request and then reuse its key with different content",
        detection="same-content replay is identified and different-content reuse is rejected",
        mitigation="enforce unique idempotency identity plus payload-hash comparison",
        recovery="only one durable side effect exists",
        postmortem="retry safety requires identity semantics, not merely retry limits",
        corrective_change="side effects must be idempotent or compensatable before automatic retry",
        retest="repeat the same idempotency key and require REPLAY without a second effect",
        verdict="PASS" if ok else "FAIL",
        observations={
            "first": first,
            "replay": replay,
            "conflict": conflict,
            "durable_effect_count": count,
            "same_failure_retest": retest,
        },
    )


def exercise_permission_failure() -> dict:
    required = "deploy:write"

    def authorized(scopes: set[str]) -> bool:
        return required in scopes

    denied = not authorized({"evidence:read"})
    recovered = authorized({"evidence:read", "deploy:write"})
    retest = not authorized({"evidence:read"})

    ok = denied and recovered and retest
    return _result(
        scenario_id="FR-05",
        title="Credential / permission failure",
        lane="L2",
        role="security-owner",
        trigger="attempt a deployment action without the required deploy:write scope",
        detection="authorization denies the action before an external side effect",
        mitigation="grant only the missing bounded capability in the drill subject",
        recovery="the authorized drill action passes without widening unrelated scopes",
        postmortem="permission failures must fail closed and identify the minimum missing authority",
        corrective_change="promotion workflows declare exact capability requirements before execution",
        retest="remove deploy:write again and require fail-closed denial",
        verdict="PASS" if ok else "FAIL",
        observations={
            "missing_scope_denied": denied,
            "minimal_scope_recovery": recovered,
            "same_failure_retest": retest,
        },
    )


def exercise_observability_blind_spot(base_url: str, source_commit: str) -> dict:
    live = _json_request(f"{base_url}/health/live")
    business = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "observability-blind-spot"),
            "expected_value": "correct",
            "observed_value": "incorrect",
            "force_failure": False,
        },
    )
    blind_spot = live.get("status") == "alive" and business.get("business_ok") is False
    recovered = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "observability-recovery"),
            "expected_value": "correct",
            "observed_value": "correct",
            "force_failure": False,
        },
    ).get("business_ok") is True
    retest = _json_request(
        f"{base_url}/v1/oracle/evaluate",
        {
            "subject": _subject(source_commit, "observability-retest"),
            "expected_value": "correct",
            "observed_value": "incorrect",
            "force_failure": False,
        },
    ).get("business_ok") is False

    ok = blind_spot and recovered and retest
    return _result(
        scenario_id="FR-06",
        title="Observability blind spot",
        lane="L3",
        role="observability-owner",
        trigger="keep HTTP liveness green while business correctness is wrong",
        detection="compare infrastructure health with the independent business oracle",
        mitigation="route incident decisions through both technical and business SLIs",
        recovery="business correctness returns to PASS without changing the evidence boundary",
        postmortem="green infrastructure metrics can coexist with a broken user outcome",
        corrective_change="alerts and rollout analysis must include a business-result signal",
        retest="recreate the liveness-green/business-fail split and require detection again",
        verdict="PASS" if ok else "FAIL",
        observations={
            "infrastructure_live": live,
            "business_failure_detected": blind_spot,
            "recovery": recovered,
            "same_failure_retest": retest,
        },
    )


def exercise_restore_assumption() -> dict:
    with tempfile.TemporaryDirectory(prefix="manager-dr-") as temp_dir:
        root = Path(temp_dir)
        active = root / "active.json"
        backup = root / "backup.json"
        original = b'{"revision":"good-v1","value":42}\n'
        active.write_bytes(original)
        shutil.copyfile(active, backup)
        expected_digest = hashlib.sha256(backup.read_bytes()).hexdigest()

        active.write_text('{"revision":"corrupt","value":null}\n', encoding="utf-8")
        detected = hashlib.sha256(active.read_bytes()).hexdigest() != expected_digest

        shutil.copyfile(backup, active)
        recovered = hashlib.sha256(active.read_bytes()).hexdigest() == expected_digest

        active.write_text('{"revision":"corrupt-again"}\n', encoding="utf-8")
        detected_again = hashlib.sha256(active.read_bytes()).hexdigest() != expected_digest
        shutil.copyfile(backup, active)
        retest = (
            detected_again
            and hashlib.sha256(active.read_bytes()).hexdigest() == expected_digest
        )

    ok = detected and recovered and retest
    return _result(
        scenario_id="FR-07",
        title="Restore / DR assumption failure",
        lane="L3",
        role="recovery-owner",
        trigger="corrupt the active bounded state after creating a known-good backup",
        detection="active-state checksum no longer matches the admitted backup subject",
        mitigation="restore only from the exact known-good backup",
        recovery="restored state checksum matches the known-good digest",
        postmortem="a backup is not recovery evidence until restore and verification are exercised",
        corrective_change="backup workflows require periodic restore tests and checksum verification",
        retest="corrupt the active state again and prove restore/verification a second time",
        verdict="PASS" if ok else "FAIL",
        observations={
            "corruption_detected": detected,
            "restore_verified": recovered,
            "same_failure_retest": retest,
            "known_good_sha256": expected_digest,
        },
    )


def _render_markdown(report: dict) -> str:
    lines = [
        "# Public failure/recovery drill receipt",
        "",
        f"Source commit: `{report['source_commit']}`",
        "",
        "Classification: **DRILL / SIMULATION**. This is not production incident history.",
        "",
        "| ID | Scenario | Lane | Verdict |",
        "|---|---|---|---|",
    ]
    for item in report["scenarios"]:
        lines.append(
            f"| {item['scenario_id']} | {item['title']} | {item['evidence_lane']} | {item['verdict']} |"
        )
    lines += [
        "",
        "Every scenario records trigger → detection → authority → mitigation → recovery → postmortem → corrective change → same-failure re-test.",
        "",
        f"Evidence ceiling: `{report['evidence_ceiling']}`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--side-inputs", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown", required=True)
    args = parser.parse_args()

    side_inputs = json.loads(Path(args.side_inputs).read_text(encoding="utf-8"))
    scenarios = [
        exercise_bad_release(args.base_url, args.source_commit),
        exercise_dependency_timeout(),
        exercise_queue_pressure(),
        exercise_duplicate_side_effect(),
        exercise_permission_failure(),
        exercise_observability_blind_spot(args.base_url, args.source_commit),
        exercise_restore_assumption(),
    ]
    passed = sum(item["verdict"] == "PASS" for item in scenarios)
    report = {
        "schema_version": "full-manager-mvp/failure-recovery-drills/v1",
        "source_commit": args.source_commit,
        "side_input_manifest": side_inputs,
        "summary": {
            "total": len(scenarios),
            "pass": passed,
            "fail": len(scenarios) - passed,
        },
        "scenarios": scenarios,
        "verdict": "PASS" if passed == len(scenarios) else "FAIL",
        "evidence_ceiling": "GITHUB_HOSTED_DETERMINISTIC_AND_LOCAL_PROCESS_FAILURE_DRILLS_ONLY",
        "not_proven": [
            "production incident history",
            "production Kubernetes recovery",
            "real customer/user impact",
            "employment or people-management tenure",
        ],
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    Path(args.markdown).write_text(_render_markdown(report), encoding="utf-8")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
