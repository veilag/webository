from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from src.callbacks import RequestApproveCallback
from src.database.models import Request
from src.states import RequestForm
from src.utils import notify_admins

router = Router()


@router.message(CommandStart())
async def handle_start_message(message: Message, state: FSMContext) -> None:
    await state.set_state(RequestForm.username)
    await message.answer("Введите имя пользователя для будущего аккаунта на сервере на латинице")


@router.message(RequestForm.username)
async def handle_username(message: Message, state: FSMContext) -> None:
    await state.update_data(username=message.text)
    await state.set_state(RequestForm.subdomain)
    await message.answer("Введите название поддомена на латинице")


@router.message(RequestForm.subdomain)
async def handle_subdomain(message: Message, state: FSMContext, bot: Bot, session: AsyncSession) -> None:
    await state.update_data(subdomain=message.text)
    data = await state.get_data()
    await state.clear()

    new_request = Request(
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username,
        username=data.get("username"),
        subdomain=data.get("subdomain")
    )

    session.add(new_request)
    await session.commit()

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(
        text="Одобрить",
        callback_data=RequestApproveCallback(request_id=new_request.id, approve=True).pack()
    ))

    await notify_admins(
        bot=bot,
        builder=keyboard,
        message=f"📝 Новая заявка. username={data.get('username')} subdomain={data.get('subdomain')}"
    )

    await message.answer("✅ Заявка отправлена")
