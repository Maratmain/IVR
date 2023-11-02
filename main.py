

from telethon.sync import TelegramClient, events
from telethon.tl import functions
from telethon.tl.custom import Button
import sqlite3
import schedule
import time

# Создание базы данных и подключение к ней
conn = sqlite3.connect('user_reminders.db')
cursor = conn.cursor()

# Создание таблицы для хранения данных о пользователях и запросах
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_reminders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        index INTEGER,
        days_before_olympiad INTEGER
    )
''')

# Сохранение изменений в базе данных
conn.commit()

# Закрытие соединения с базой данных
conn.close()

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
            await event.respond(message, buttons=buttons, link_preview=False)
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
                [Button.inline("МОШ", b"/mosh"), Button.inline("Vseross", b"/vseross")]
            ]
            await event.respond("Физика:", buttons=buttons)
            user_selections[chat_id]["subject"] = "Физика"

        @client.on(events.CallbackQuery(data=b"/mosh"))
        async def mosh(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("Напоминание", b"/mosh_reminder"), Button.inline("Материалы", b"/mosh_materials"), Button.inline("Сайт", b"/mosh_site")],
                [Button.inline("Факультативы по подготовке", b"/mosh_electives"), Button.inline("Об олимпиаде", b"/mosh_info")]
            ]
            await event.respond("МОШ:", buttons=buttons)
            user_selections[chat_id]["subject_type"] = "МОШ"

        @client.on(events.CallbackQuery(data=b"/vseross"))
        async def vseross(event):
            chat_id = event.chat_id
            buttons = [
                [Button.inline("Нapomинание", b"/vseross_reminder"), Button.inline("Материалы", b"/vseross_materials"), Button.inline("Сайт", b"/vseross_site")],
                [Button.inline("Факультативы по подготовке", b"/vseross_electives"), Button.inline("Об олимпиаде", b"/vseross_info")]
            ]
            await event.respond("Всеросс:", buttons=buttons)
            user_selections[chat_id]["subject_type"] = "Всеросс"

        @client.on(events.CallbackQuery(data=b"/mosh_reminder"))
        async def mosh_reminder(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")

            if subject_type == "МОШ":
                buttons = [
                    [Button.inline("За неделю", b"/mosh_reminder_week"), Button.inline("За 3 дня", b"/mosh_reminder_3days"), Button.inline("За день", b"/mosh_reminder_1day")]
                ]
                await event.respond("Олимпиада МОШ будет проходить 4 ноября. Выберите, когда Вам напомнить о предстоящем событии:", buttons=buttons)

                # Здесь добавьте код для записи выбора пользователя в базу данных
                selected_index = user_selections.get(chat_id, {}).get("index")
                if selected_index is not None:
                    # Проверка, чтобы индекс записывался только один раз
                    cursor.execute('INSERT OR REPLACE INTO user_reminders (user_id, index, days_before_olympiad) VALUES (?, ?, ?)',
                                (chat_id, selected_index, 3))
                    conn.commit()
            else:
                await event.respond("Напоминание доступно только для МОШ")

        @client.on(events.CallbackQuery(data=b"/vseross_reminder"))
        async def vseross_reminder(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")

            if subject_type == "Всеросс":
                buttons = [
                    [Button.inline("За неделю", b"/vseross_reminder_week"), Button.inline("За 3 дня", b"/vseross_reminder_3days"), Button.inline("За день", b"/vseross_reminder_1day")]
                ]
                await event.respond("Олимпиада Всеросс будет проходить 10 ноября. Выберите, когда Вам напомнить о предстоящем событии:", buttons=buttons)

        @client.on(events.CallbackQuery(data=b"/mosh_reminder_week"))
        async def mosh_reminder_week(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за неделю до проведения.")

        @client.on(events.CallbackQuery(data=b"/mosh_reminder_3days"))
        async def mosh_reminder_3days(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за 3 дня до проведения.")

        @client.on(events.CallbackQuery(data=b"/mosh_reminder_1day"))
        async def mosh_reminder_1day(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за день до проведения.")

        @client.on(events.CallbackQuery(data=b"/vseross_reminder_week"))
        async def vseross_reminder_week(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за неделю до проведения.")

        @client.on(events.CallbackQuery(data=b"/vseross_reminder_3days"))
        async def vseross_reminder_3days(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за 3 дня до проведения.")

        @client.on(events.CallbackQuery(data=b"/vseross_reminder_1day"))
        async def vseross_reminder_1day(event):
            chat_id = event.chat_id
            await event.respond("Напомним Вам ровно в 12:00 по московскому времени за день до проведения.")

        @client.on(events.CallbackQuery(data=b"/send_reminder"))
        async def send_reminder(user_id):
            # Здесь вы можете получить информацию о пользователе, олимпиаде и днях до олимпиады из базы данных SQL
            conn = sqlite3.connect('user_reminders.db')
            cursor = conn.cursor()

            # Получить информацию о пользователе
            cursor.execute("SELECT olympiad_index, days_before FROM user_reminders WHERE user_id=?", (user_id,))
            result = cursor.fetchone()

            if result:
                olympiad_index, days_before = result
                # Получите информацию о конкретной олимпиаде по olympiad_index
                # Затем, используя полученные данные, сформируйте сообщение с напоминанием
                # и отправьте его пользователю в нужное время

                # Пример: Получение информации о конкретной олимпиаде
                # olympiad_data = get_olympiad_data(olympiad_index)

                # Здесь формируется сообщение с напоминанием
                message = f"Напоминание об олимпиаде {olympiad_data['name']}, которая пройдет через {days_before} дней"

                # Затем отправка сообщения пользователю (здесь нужно использовать ваш код для отправки сообщений)

            conn.close()

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

        @client.on(events.CallbackQuery(data=b"/mosh_electives"))
        async def mosh_electives(event):
            chat_id = event.chat_id
            days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            buttons = [Button.inline(day, f"/elective_{day}") for day in days_of_week]
            await event.respond("Выберите удобный день:", buttons=buttons)

        @client.on(events.CallbackQuery(data=b"/mosh_info"))
        async def mosh_info(event):
            chat_id = event.chat_id
            subject_type = user_selections.get(chat_id, {}).get("subject_type")
            
            if subject_type == "МОШ":
                message = "Московская олимпиада школьников (МОШ) - это престижное соревнование, проводимое в Москве. "
                message += "Она предоставляет школьникам уникальную возможность проявить свои знания и навыки в различных предметах. "
                message += "Участие в МОШ может открыть двери в лучшие образовательные учреждения страны. "
                message += "Для получения подробной информации посетите официальный сайт МОШ."
                
            elif subject_type == "Всеросс":
                message = "Всероссийская олимпиада школьников - это масштабное мероприятие, которое объединяет школьников "
                message += "из разных регионов России. Она позволяет выявить и поддержать талантливых учеников. "
                message += "Для получения подробной информации посетите официальный сайт Всеросс."
                
            else:
                message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."
            
            await event.respond(message)

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
