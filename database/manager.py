from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from config import config

master_engine = create_async_engine(
    url=config.database.master_database_url, echo=False, pool_size=20, max_overflow=10
)

slave_engine = create_async_engine(
    url=config.database.slave_database_url, echo=False, pool_size=20, max_overflow=10
)

master_db = async_sessionmaker(master_engine, expire_on_commit=False)
slave_db = async_sessionmaker(slave_engine, expire_on_commit=False)


@asynccontextmanager
async def get_master_session() -> AsyncSession:
    async with master_db() as session:
        yield session


@asynccontextmanager
async def get_slave_session() -> AsyncSession:
    async with slave_db() as session:
        yield session


async def dispose_engines():
    await master_engine.dispose()
    await slave_engine.dispose()
