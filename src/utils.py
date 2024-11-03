from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

admins = [898008765]


async def notify_admins(bot: Bot, builder: InlineKeyboardBuilder, message: str):
    for admin_id in admins:
        await bot.send_message(
            chat_id=admin_id,
            reply_markup=builder.as_markup(),
            text=message
        )
