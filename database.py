from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


class DatabaseHelper:

    def __init__(self):
        self.engine = create_async_engine(url=settings.database_url, echo=settings.db_echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )
