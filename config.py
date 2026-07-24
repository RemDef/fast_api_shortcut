from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    database_url: str = Field(
        default=f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3", alias="DB_URL"
    )
    jwt_secret_key: str = Field(default="some_secret_key", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env"}
    # db_echo только в режиме отладки!
    db_echo: bool = False


settings = Settings()
