from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

_REQUESTS = Counter(
    "manager_demo_http_requests_total",
    "HTTP requests handled by the public demo control plane.",
    ["method", "route", "status"],
)
_LATENCY = Histogram(
    "manager_demo_http_request_duration_seconds",
    "Request duration used by the demo latency SLI.",
    ["method", "route"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
_IN_FLIGHT = Gauge(
    "manager_demo_http_in_flight",
    "Requests currently executing.",
)
_BUSINESS = Counter(
    "manager_demo_business_oracle_total",
    "Business-oracle outcomes; infrastructure success must not imply business success.",
    ["verdict"],
)


def configure_tracing(service_name: str = "full-manager-mvp-control-plane") -> None:
    current = trace.get_tracer_provider()
    if isinstance(current, TracerProvider):
        return
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    trace.set_tracer_provider(provider)


class RequestTelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        tracer = trace.get_tracer("manager-demo.http")
        route = request.url.path
        method = request.method
        started = time.perf_counter()
        _IN_FLIGHT.inc()
        status_code = 500
        try:
            with tracer.start_as_current_span(f"{method} {route}") as span:
                span.set_attribute("http.request.method", method)
                span.set_attribute("url.path", route)
                response = await call_next(request)
                status_code = response.status_code
                span.set_attribute("http.response.status_code", status_code)
                context = span.get_span_context()
                response.headers["X-Trace-Id"] = f"{context.trace_id:032x}"
                return response
        finally:
            _IN_FLIGHT.dec()
            _REQUESTS.labels(method=method, route=route, status=str(status_code)).inc()
            _LATENCY.labels(method=method, route=route).observe(time.perf_counter() - started)


def record_business_oracle(ok: bool) -> None:
    _BUSINESS.labels(verdict="PASS" if ok else "FAIL").inc()


def install_observability(app: FastAPI) -> None:
    configure_tracing()
    app.add_middleware(RequestTelemetryMiddleware)

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> StarletteResponse:
        return StarletteResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
