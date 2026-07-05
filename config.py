from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(
        default="sqlite+aiosqlite:///./db.sqlite3",
        alias="DB_URL"
    )

    model_config = {"env_file": ".env"}
    # db_echo только в режиме отладки!
    db_echo: bool = False


settings = Settings()
