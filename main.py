import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.router import router
from common.models import Base
from database import db_helper
from middleware.logging import LoggingMiddleware
from tasks.models import Task  # noqa: F401
from users.models import User  # noqa: F401

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 3,
    },
)

app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type]

app.include_router(router)


@app.get("/check_site")
def check_site_work():
    return "Hello World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, reload_dirs=["."], port=7994)
