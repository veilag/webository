from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./data.db"
engine = create_async_engine(DATABASE_URL)

Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession
)


async def get_db():
    async with Session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
