import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import cache.dependencies as cache_dependencies
import middleware.rate_limit as rate_limit_middleware
from auth.jwt import create_access_token
from cache.dependencies import get_cache
from common.models import Base
from database import get_session
from main import app
from tasks.models import Task  # noqa: F401
from tests.factories import UserFactory
from tests.fake_cache import FakeCacheBackend
from users.models import User  # noqa: F401

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(session_factory):
    fake_cache = FakeCacheBackend()

    app.dependency_overrides[get_cache] = lambda: fake_cache

    cache_dependencies.cache_backend = fake_cache

    rate_limit_middleware.cache_backend = fake_cache

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(db_session):
    obj = UserFactory.build()
    db_session.add(obj)
    await db_session.commit()
    await db_session.refresh(obj)
    return obj


@pytest_asyncio.fixture
async def auth_headers(user):
    token = create_access_token(user_id=user.id)
    return {"Authorization": f"Bearer {token}"}
