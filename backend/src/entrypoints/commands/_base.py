from collections.abc import Callable

from config import get_db_dsn_for_environment, AppConfig, LogLevel
from log_config import configure_logging
from shared.db import DatabaseAdapter, populate_base


async def db_command(
    command: Callable,
    config: AppConfig = AppConfig(),
) -> None:
    configure_logging(LogLevel.info, False)
    db_dsn = get_db_dsn_for_environment(config)
    db_adapter = DatabaseAdapter(
        dsn=db_dsn,
        echo=False,
        pool_size=config.db.pool_size,
        pool_max_overflow=config.db.pool_max_overflow,
    )
    populate_base()

    async with db_adapter.session_factory() as session:
        await command(session)
