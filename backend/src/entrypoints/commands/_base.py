from collections.abc import Callable

from config import (
    get_db_dsn_for_environment,
    AppConfig,
    configure_logging,
    LogLevel,
)
from shared.db import DatabaseAdapter, populate_base


async def db_command(
    command: Callable,
    config: AppConfig = AppConfig(),
) -> None:
    configure_logging(LogLevel.info, False)
    db_dsn = get_db_dsn_for_environment(config)
    db_adapter = DatabaseAdapter(
        db_dsn=db_dsn,
        echo=False,
        pool_size=config.pool_size,
        pool_max_overflow=config.pool_max_overflow,
    )
    populate_base()

    async with db_adapter.session_factory() as session:
        await command(session)
