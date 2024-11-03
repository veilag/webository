from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .base import Base
from .models import Request


async def setup_database():
    engine = create_async_engine(url="sqlite+aiosqlite:///./data.db")
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine, sessionmaker


__all__ = [
    "Base",
    "Request",
    "setup_database"
]