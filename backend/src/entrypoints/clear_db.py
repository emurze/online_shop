import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from config import AppConfig, get_db_dsn_for_environment
from main import create_app
from shared.db import DatabaseAdapter, Base

lg = logging.getLogger(__name__)


def populate_base():
    create_app()


async def clear_db(session: AsyncSession) -> None:
    for table in reversed(Base.metadata.sorted_tables):
        lg.debug(f"Clearing table {table}")
        await session.execute(table.delete())
    else:
        await session.commit()


async def main(config=AppConfig()) -> None:
    db_dsn = get_db_dsn_for_environment(config)
    db_adapter = DatabaseAdapter(db_dsn=db_dsn, echo=True)
    populate_base()

    async with db_adapter.session_factory() as session:
        await clear_db(session)


if __name__ == "__main__":
    asyncio.run(main())
