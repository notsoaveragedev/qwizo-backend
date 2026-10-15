import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger("http")

QUIET_PATHS = {"/health", "/ready"}

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
}


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        started = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        finally:
            if request.url.path not in QUIET_PATHS or status_code >= 500:
                log = logger.error if status_code >= 500 else logger.info
                log(
                    "request",
                    method=request.method,
                    path=request.url.path,
                    status=status_code,
                    duration_ms=round((time.perf_counter() - started) * 1000, 1),
                    ip=request.client.host if request.client else None,
                )

        response.headers["X-Request-ID"] = request_id
        response.headers.update(SECURITY_HEADERS)
        return response
