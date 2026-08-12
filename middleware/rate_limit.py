import logging

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cache.dependencies import cache_backend
from cache.rate_limit import is_rate_limit_allowed
from common.auth import get_user_id_from_token
from config import settings

logger = logging.getLogger("rate_limit")


def _client_key(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
        user_id = get_user_id_from_token(token)
        if user_id:
            return f"ratelimit:user:{user_id}"

    ip = request.client.host if request.client else "unknown"
    return f"ratelimit:ip:{ip}"


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # блочим ли swagger/redoc
        # if request.url.path in {"/docs", "/openapi.json", "/redoc"}:
        #     return await call_next(request)

        key = _client_key(request)
        allowed = await is_rate_limit_allowed(
            cache_backend,
            key,
            max_requests=settings.rate_limit_requests,
            rate_limit_seconds=settings.rate_limit_seconds,
        )
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests"},
            )
        return await call_next(request)
