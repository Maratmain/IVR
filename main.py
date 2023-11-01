api_id = 26730332
api_hash = '444cac746aea62c94690b4217f412c9e'
bot_token = '6643259676:AAHuAQXWS4dZZSV17ql6vP2v19cxaBpWMbc'

from telethon.sync import TelegramClient, events
from telethon.tl import functions
from telethon.tl.custom import Button

# Словарь для отслеживания пользователей, которые начали разговор
started_conversations = {}

# Словарь для хранения выбора пользователей
user_selections = {}

# Словарь для хранения ссылок
urls = {
    "Математика": {
        "МОШ": {
            "Материалы": "https://mos.olimpiada.ru/tasks/math",
            "Сайт": "https://mos.olimpiada.ru/olymp/math"
        },
        "Всеросс": {
            "Материалы": "https://olimpiada.ru/activity/72/tasks",
            "Сайт": "https://vos.olimpiada.ru/math/2023_2024"
        }
    },
    "Программирование": {
        "МОШ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://mos-inf.olimpiada.ru/"
        },
        "Всеросс": {
            "Материалы": "https://olimpiada.ru/activity/73/tasks",
            "Сайт": "https://olympiads.ru/moscow/2023-24/vsosh/index.shtml"
        }
    }
}

async def send_recommendation(client, chat_id):
    # Проверяем, начинал ли пользователь разговор ранее
    if chat_id not in started_conversations:
        message, buttons = start_message()
        await client.send_message(chat_id, message, buttons=buttons, link_preview=False)

def start_message():
    message = "Начните работать с Вашим личным олимпиадным помощником!"
    buttons = [
        [Button.inline("Закончить диалог", b"/end"), Button.inline("Выбор олимпиад", b"/subjects"), Button.inline("Другое", b"/other")]
    ]
    return message, buttons

async def main():
    async with TelegramClient('bot_session', api_id, api_hash) as client:
        @client.on(events.NewMessage(pattern='/start'))
        async def start(event):
            chat_id = event.chat_id
            message, buttons = start_message()
            await event.respond(message, buttons=buttons)

            # Отмечаем пользователя как начавшего разговор
            started_conversations[chat_id] = True
            user_selections[chat_id] = {}

        @client.on(events.CallbackQuery(data=b"/end"))
        async def end(event):
            chat_id = event.chat_id
            await event.respond("Работа завершена. Удачи!")
            await event.respond("Для активации бота снова, нажмите /start.")
            await send_recommendation(client, chat_id)

        @client.on(events.CallbackQuery(data=b"/other"))
        async def other(event):
            # Добавьте обработку других команд здесь
            await event.respond("Вы выбрали 'Другое'. Добавьте соответствующий обработчик для этой команды.")
            await send_recommendation(client, chat_id)

        @client.on(events.CallbackQuery(data=b"/subjects"))
        async def subjects(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("Математика", b"/math"), Button.inline("Русский", b"/russian")],
                [Button.inline("Программирование", b"/programming"), Button.inline("Экономика", b"/economics")],
                [Button.inline("Физика", b"/physics")]
            ]
            await event.respond("Предметы:", buttons=buttons)

        @client.on(events.CallbackQuery(data=b"/math"))
        async def math(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
            ]
            await event.respond("Математика:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Математика"

        @client.on(events.CallbackQuery(data=b"/russian"))
        async def russian(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
            ]
            await event.respond("Русский:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Русский"

        @client.on(events.CallbackQuery(data=b"/programming"))
        async def programming(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
            ]
            await event.respond("Программирование:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Программирование"

        @client.on(events.CallbackQuery(data=b"/economics"))
        async def economics(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
            ]
            await event.respond("Экономика:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Экономика"

        @client.on(events.CallbackQuery(data=b"/physics"))
        async def physics(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
            ]
            await event.respond("Физика:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Физика"

        @client.on(events.CallbackQuery(data=b"/mosh"))
        async def mosh(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("Напоминание", b"/mosh_reminder"), Button.inline("Материалы", b"/mosh_materials"), Button.inline("Сайт", b"/mosh_site")]
            ]
            await event.respond("МОШ:", buttons=buttons)
            user_selections[chat_id]["subject_type"] = "МОШ"

        @client.on(events.CallbackQuery(data=b"/vseross"))
        async def vseross(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("Напоминание", b"/vseross_reminder"), Button.inline("Материалы", b"/vseross_materials"), Button.inline("Сайт", b"/vseross_site")]
            ]
            await event.respond("Всеросс:", buttons=buttons)
            user_selections[chat_id]["subject_type"] = "Всеросс"

        @client.on(events.CallbackQuery(data=b"/mosh_reminder"))
        async def mosh_reminder(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            await event.respond(f"{subject_type} Напоминание")

        @client.on(events.CallbackQuery(data=b"/vseross_reminder"))
        async def vseross_reminder(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            await event.respond(f"{subject_type} Напоминание")

        @client.on(events.CallbackQuery(data=b"/mosh_materials"))
        async def mosh_materials(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            subject = user_selections.get(chat_id, {}).get("subject")
            url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")

            if subject_type == "МОШ" and url:
                await event.respond("Архив заданий МОШ", buttons=[Button.url("Материалы", url)])
            elif subject_type == "Всеросс" and url:
                await event.respond("Материалы", buttons=[Button.url("Материалы", url)])
            else:
                await event.respond("Ссылка не найдена")

        @client.on(events.CallbackQuery(data=b"/vseross_materials"))
        async def vseross_materials(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            subject = user_selections.get(chat_id, {}).get("subject")
            url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")

            if url:
                await event.respond("Архив заданий Всеросс", buttons=[Button.url("Материалы", url)])
            else:
                await event.respond("Ссылка не найдена")

        @client.on(events.CallbackQuery(data=b"/mosh_site"))
        async def mosh_site(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            subject = user_selections.get(chat_id, {}).get("subject")
            url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

            if url:
                await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
            else:
                await event.respond("Ссылка не найдена")

        @client.on(events.CallbackQuery(data=b"/vseross_site"))
        async def vseross_site(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            subject = user_selections.get(chat_id, {}).get("subject")
            url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

            if url:
                await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
            else:
                await event.respond("Ссылка не найдена")

        print("Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
