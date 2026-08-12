import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from common.redact import redact_body

logger = logging.getLogger("http")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        request_body = await request.body()
        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        duration_ms = (time.perf_counter() - start) * 1000

        content_type = request.headers.get("content-type")
        safe_req = redact_body(
            request_body.decode("utf-8", errors="replace"),
            content_type,
        )
        safe_resp = redact_body(
            response_body.decode("utf-8", errors="replace"),
            response.headers.get("content-type"),
        )
        logger.info(
            "%s %s | status=%s | %.2fms | req=%s | resp=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            safe_req,
            safe_resp,
        )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
