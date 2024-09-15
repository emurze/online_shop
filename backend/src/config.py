import os
from pathlib import Path
from typing import Literal

import logging
from pydantic import SecretStr, BaseModel, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
BASE_DIR: Path = Path(__file__).parent
CERTS_DIR: Path = BASE_DIR.parent / "certs"
MODULES_DIR: Path = BASE_DIR / "api_v1"


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseModel):
    pool_size: int = 10
    pool_max_overflow: int = 0
    echo: bool = False
    dsn: str = "postgresql+asyncpg://postgres:password@db:5432/postgres"
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str = (
        "bbfd51be4a928196ed823f2c2061e38196db23d32190992f596d2a225d067ac1"
    )
    verification_token_secret: str = (
        "e2ac3c91cf360b0ad741a3d1b6b9e8162a8fffa1ccd6b3d60f9b66c152356d8f"
    )


# class AuthJWTConfig(BaseModel):
#     private_key_path: Path = CERTS_DIR / "jwt-private.pem"
#     public_key_path: Path = CERTS_DIR / "jwt-public.pem"
#     algorithm: str = "RS256"
#     access_token_expire_minutes: int = 15
#     refresh_token_expire_days: int = 30


class ApiConfig(BaseModel):
    v1_prefix: str = "/api/v1"
    title: str = "App"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    secret_key: SecretStr = "secret"
    debug: bool = True
    allowed_origins: list[str] = [
        "http://localhost:3000",
    ]


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.template", ".env"],
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        extra="allow",
    )
    api: ApiConfig = Field(default_factory=ApiConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    access_token: AccessToken = Field(default_factory=AccessToken)


def get_db_dsn_for_environment(config: Config) -> str:
    """
    Get database url for entrypoint inside docker container or localhost.
    Allows you to run your commands outside container.
    """

    if os.getenv("IS_DOCKER_CONTAINER"):
        return config.db.dsn

    return config.db.dsn.replace("db", "localhost")


def configure_logging(config: Config) -> None:
    logging.basicConfig(
        level=config.logging.log_level,
        format=config.logging.log_format,
    )


app_config = Config()  # global
