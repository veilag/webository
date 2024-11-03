import subprocess
from os import getenv

import requests
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from password_generator import PasswordGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.callbacks import RequestApproveCallback
from src.crud import get_request_by_id

router = Router()
pwo = PasswordGenerator()


@router.callback_query(RequestApproveCallback.filter(F.approve))
async def handle_approve_request(query: CallbackQuery, callback_data: RequestApproveCallback, session: AsyncSession, bot: Bot):
    request = await get_request_by_id(
        session=session,
        id=callback_data.request_id
    )

    await bot.send_message(chat_id=request.telegram_id, text="✅ Ваша заявка одобрена")
    process_message = await bot.send_message(chat_id=request.telegram_id, text="🔄 Создаю пользователя")

    user_password = pwo.generate()
    user_setup_process = subprocess.Popen([
        './scripts/user_setup.sh',
        request.username, user_password
    ])

    stdout, stderr = user_setup_process.communicate()

    if user_setup_process.returncode != 0:
        await process_message.edit_text("❌ Ошибка при создании пользователя. Логи отправлены училке")
        await query.message.answer(f"Ошибка при создании пользователя tg_username={request.telegram_username}.\n\n*stdout*\n{stdout}\n\nstderr\n{stderr}")
        return

    await process_message.edit_text("🔄 Создаю конфигурацию NGINX")

    nginx_setup_process = subprocess.Popen([
        './scripts/nginx_setup.sh',
        f'{request.subdomain}.webository.ru', request.username
    ])

    stdout, stderr = nginx_setup_process.communicate()

    if user_setup_process.returncode != 0:
        await process_message.edit_text("❌ Ошибка при конфигурации NGINX. Логи отправлены училке")
        await query.message.answer(f"Ошибка при NGINX tg_username={request.telegram_username}.\n\n*stdout*\n{stdout}\n\nstderr\n{stderr}")
        return

    await process_message.edit_text("🔄 Создаю конфигурацию GUNICORN")

    gunicorn_setup_process = subprocess.Popen([
        './scripts/gunicorn_setup.sh',
        request.username
    ])

    stdout, stderr = gunicorn_setup_process.communicate()

    if user_setup_process.returncode != 0:
        await process_message.edit_text("❌ Ошибка при конфигурации GUNICORN. Логи отправлены училке")
        await query.message.answer(
            f"Ошибка при GUNICORN tg_username={request.telegram_username}.\n\n*stdout*\n{stdout}\n\nstderr\n{stderr}")
        return

    await process_message.edit_text(
        f"✅ *Пользователь создан и настроен*\n\n*Логин*: {request.username}\n*Пароль*: {user_password}"
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getenv('TIMEWEB_TOKEN'),
    }

    response = requests.post(
        f'https://api.timeweb.cloud/api/v1/domains/webository.ru/subdomains/{request.subdomain}',
        headers=headers,
    )

    print(response.json())

    json_data = {
        'type': 'A',
        'value': '213.171.12.197',
    }

    response = requests.post(
        f'https://api.timeweb.cloud/api/v1/domains/{request.subdomain}.webository.ru/dns-records', headers=headers,
        json=json_data
    )

    print(response.json())
