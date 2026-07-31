import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.models import Base
from database import get_session
from main import app
from tasks.models import Task  # noqa: F401
from users.models import User  # noqa: F401

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def auth_headers(client):
    user = {
        "username": "task_user",
        "email": "task_user@example.com",
        "password": "Qwerty1!",
        "first_name": "Task",
        "last_name": "User",
        "birthdate": "1995-01-15",
    }
    await client.post("/v1/users/register", json=user)

    login = await client.post(
        "/v1/auth/login",
        data={"username": user["username"], "password": user["password"]},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
