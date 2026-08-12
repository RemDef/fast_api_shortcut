import pytest_asyncio
from httpx import ASGITransport, AsyncClient

import cache.dependencies as cache_dependencies
import middleware.rate_limit as rate_limit_middleware
from auth.jwt import create_access_token
from cache.dependencies import get_cache
from database import get_session
from main import app
from tests.factories import UserFactory
from tests.fake_cache import FakeCacheBackend


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
async def auth_headers(user):
    token = create_access_token(user_id=user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def logged_in_client(client, auth_headers):
    client.headers.update(auth_headers)
    return client


@pytest_asyncio.fixture
async def other_user(db_session):
    obj = UserFactory.build()
    db_session.add(obj)
    await db_session.commit()
    await db_session.refresh(obj)
    return obj


@pytest_asyncio.fixture
async def other_auth_headers(other_user):
    token = create_access_token(user_id=other_user.id)
    return {"Authorization": f"Bearer {token}"}
