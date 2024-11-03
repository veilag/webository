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


def add_subdomain(request):
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


@router.callback_query(RequestApproveCallback.filter(F.approve))
async def handle_approve_request(query: CallbackQuery, callback_data: RequestApproveCallback, session: AsyncSession, bot: Bot):
    request = await get_request_by_id(
        session=session,
        id=callback_data.request_id
    )

    await bot.send_message(chat_id=request.telegram_id, text="✅ Ваша заявка одобрена. Начинаю настройку вашего аккаунта")
    process_message = await bot.send_message(chat_id=request.telegram_id, text="🔄 Создаю пользователя")

    user_password = pwo.generate()
    subprocess.Popen([
        './scripts/user_setup.sh',
        request.username, user_password
    ])

    await process_message.edit_text("🔄 Настраиваю поддомен")
    add_subdomain(request)

    await process_message.edit_text("🔄 Создаю конфигурацию nginx и получаю сертификат")

    subprocess.Popen([
        './scripts/nginx_setup.sh',
        f'{request.subdomain}.webository.ru', request.username
    ])

    await process_message.edit_text("🔄 Создаю конфигурацию gunicorn")

    subprocess.Popen([
        './scripts/gunicorn_setup.sh',
        request.username
    ])

    await process_message.edit_text(
        f"""✅ Пользователь успешно создан и настроен

Твои данные для входа 👉
Логин: {request.username}
Пароль: <span class="tg-spoiler">{user_password}</span>

———
Для того, чтобы подключится к серверу нужен ssh клиент, он уже есть, если ты работаешь с линукса, тогда используй команду

<pre language="bash">
ssh user@webository.ru
</pre>
где user — твой логин
""",
        parse_mode="HTML"
    )
