from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    database_url: str = Field(
        # default=f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3", alias="DB_URL"
        default="postgresql+asyncpg://app:app@localhost:5432/app",
        alias="DB_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    cache_ttl_seconds: int = 3600
    rate_limit_requests: int = Field(
        default=100,
        alias="RATE_LIMIT_REQUESTS",
    )
    rate_limit_seconds: int = Field(
        default=60,
        alias="RATE_LIMIT_SECONDS",
    )
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    jwt_secret_key: str = Field(default="some_secret_key", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env"}
    # db_echo только в режиме отладки!
    db_echo: bool = False


settings = Settings()
