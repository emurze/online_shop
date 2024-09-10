import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from entrypoints.commands._base import db_command
from shared.db import Base

lg = logging.getLogger(__name__)


async def clear_db(session: AsyncSession) -> None:
    for table in reversed(Base.metadata.sorted_tables):
        lg.debug(f"Clearing table {table}")
        await session.execute(table.delete())
    else:
        await session.commit()


if __name__ == "__main__":
    asyncio.run(db_command(clear_db))
