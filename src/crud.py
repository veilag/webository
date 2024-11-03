from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Request


async def get_request_by_id(session: AsyncSession, id: int) -> Request | None:
    result = await session.execute(
        select(Request)
        .where(Request.id == id)
    )

    return result.scalar_one_or_none()
