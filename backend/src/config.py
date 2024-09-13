import os
from pathlib import Path

from pydantic import SecretStr, BaseModel, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

from log_config import LogLevel

BASE_DIR: Path = Path(__file__).parent


class DatabaseConfig(BaseModel):
    pool_size: int = 10
    pool_max_overflow: int = 0
    echo: bool = False
    dsn: str = "postgresql+asyncpg://postgres:password@db:5432/postgres"


class RedisConfig(BaseModel):
    dsn: str = "redis://db:6379/0"


class AuthJWTConfig(BaseModel):
    certs_dir: Path = BASE_DIR.parent / "certs"
    private_key_path: Path = certs_dir / "jwt-private.pem"
    public_key_path: Path = certs_dir / "jwt-public.pem"


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    api_v1_prefix: str = "/api/v1"
    app_title: str = "App"
    allowed_origins: list[str] = [
        "http://localhost:3000",
    ]
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    version: str = "0.0.0"
    secret_key: SecretStr = "secret"
    debug: bool = True
    log_level: LogLevel | None = None
    modules_dir_name: Path = "api_v1"
    modules_dir: Path = BASE_DIR / modules_dir_name
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    auth_jwt: AuthJWTConfig = Field(default_factory=AuthJWTConfig)


def get_db_dsn_for_environment(app_config: AppConfig = AppConfig()) -> str:
    """
    Get database url for entrypoint inside docker container or localhost.
    Allows you to run your commands outside container.
    """

    if os.getenv("IS_DOCKER_CONTAINER"):
        return app_config.db.dsn

    return app_config.db.dsn.replace("db", "localhost")


config = AppConfig()  # global
