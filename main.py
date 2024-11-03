import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.database import setup_database
from src.middlewares.db import DbSessionMiddleware
from src.routers.request import router as request_router
from src.routers.admin import router as admin_router
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    engine, sessionmaker = await setup_database()

    bot = Bot(getenv("TELEGRAM_TOKEN"), default=DefaultBotProperties(
        parse_mode="Markdown"
    ))

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(request_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
