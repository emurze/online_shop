import logging
from enum import Enum

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings

LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)


class LogLevel(str, Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str | None, debug: bool) -> None:
    if not log_level:
        log_level = LogLevel.debug if debug else LogLevel.warning

    log_level = log_level.upper()

    if log_level not in list(LogLevel):
        # We use LogLevel.error as the default log level
        logging.basicConfig(level=LogLevel.error)

    elif log_level == LogLevel.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # FastAPI
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

    # Postgres
    pool_size: int = 10
    pool_max_overflow: int = 0
    db_echo: bool = False
    db_dsn: str = "postgresql+asyncpg://postgres:password@db:5432/postgres"
