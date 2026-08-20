import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from common.models import Base
from tests.factories import TaskFactory, UserFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def user_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    return UserFactory


@pytest_asyncio.fixture
async def user(user_factory):
    return await user_factory.create()


@pytest.fixture
def task_factory(db_session):
    TaskFactory._meta.sqlalchemy_session = db_session
    return TaskFactory


@pytest_asyncio.fixture
async def task(task_factory, user):
    return await task_factory.create(user_id=user.id)


@pytest_asyncio.fixture
async def tasks(task_factory, user):
    return await task_factory.create_batch(3, user_id=user.id)
