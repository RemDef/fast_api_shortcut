import logging
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI

from api.router import router
from config import settings
from middleware.logging import LoggingMiddleware
from middleware.rate_limit import RateLimitMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        send_default_pii=False,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 3,
    },
)

app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type]
app.add_middleware(RateLimitMiddleware)  # type: ignore[arg-type]

app.include_router(router)


@app.get("/check_site")
def check_site_work():
    return "Hello World!"


@app.get("/sentry-debug")
def trigger_error():
    raise ZeroDivisionError("sentry test")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, reload_dirs=["."], port=7995)
