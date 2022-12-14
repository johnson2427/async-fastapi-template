import asyncio
import logging

from app.db.init_db import init_db
from app.db.postgres.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with SessionLocal() as session:  # type: ignore
        await init_db(session)


async def main() -> None:
    logger.info("Creating initial data")
    asyncio.create_task(init())


if __name__ == "__main__":
    asyncio.run(main())
