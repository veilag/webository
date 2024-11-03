from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart())
async def handle_start_message(message: Message, session: AsyncSession):
    await message.answer("Hello, world")

