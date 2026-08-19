from __future__ import annotations

import argparse
import json
import time
import urllib.request


def request_json(url: str, *, payload: dict[str, object] | None = None, method: str | None = None) -> object:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=5) as response:
        body = response.read()
    return json.loads(body) if body else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://127.0.0.1:8474")
    parser.add_argument("--proxy-url", default="http://127.0.0.1:18081/health.txt")
    parser.add_argument("--latency-ms", type=int, default=450)
    args = parser.parse_args()
    if not 100 <= args.latency_ms <= 1000:
        raise SystemExit("latency injection must stay bounded to 100..1000 ms")

    api = args.api.rstrip("/")
    # Remove stale proxy from a previous interrupted run.
    try:
        request_json(f"{api}/proxies/manager-upstream", method="DELETE")
    except Exception:
        pass

    request_json(
        f"{api}/proxies",
        payload={"name": "manager-upstream", "listen": "127.0.0.1:18081", "upstream": "127.0.0.1:18080", "enabled": True},
    )
    request_json(
        f"{api}/proxies/manager-upstream/toxics",
        payload={
            "name": "bounded-latency",
            "type": "latency",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"latency": args.latency_ms, "jitter": 0},
        },
    )

    started = time.perf_counter()
    with urllib.request.urlopen(args.proxy_url, timeout=5) as response:
        body = response.read().decode().strip()
    elapsed_ms = (time.perf_counter() - started) * 1000
    if body != "upstream-ok":
        raise SystemExit("proxy returned unexpected body")
    if elapsed_ms < args.latency_ms * 0.8:
        raise SystemExit(f"fault injection was not observed: {elapsed_ms:.1f} ms")

    request_json(f"{api}/proxies/manager-upstream", method="DELETE")
    proxies = request_json(f"{api}/proxies")
    if isinstance(proxies, list) and any(item.get("name") == "manager-upstream" for item in proxies):
        raise SystemExit("proxy cleanup failed")
    print(json.dumps({"verdict": "PASS", "latency_ms": round(elapsed_ms, 1), "injected_ms": args.latency_ms, "cleanup": "PASS"}))


if __name__ == "__main__":
    main()
