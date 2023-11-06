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
        "ММО": {
            "Материалы": "https://mos.olimpiada.ru/tasks/math",
            "Сайт": "https://mmo.mccme.ru/"
        },
        "ВОШ": {
            "Материалы": "https://olimpiada.ru/activity/72/tasks",
            "Сайт": "https://vos.olimpiada.ru/math/2023_2024"
        },
        "Турнир городов": {
            "Материалы": "https://www.turgor.ru/problems/",
            "Сайт": "https://www.turgor.ru/"
        },
        "Высшая проба": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-math",
            "Сайт": "https://olymp.hse.ru/mmo/math"
        },
        "Физтех": {
            "Материалы": "https://olymp.mipt.ru/olympiad/samples",
            "Сайт": "https://olymp-online.mipt.ru/"
        },
        "Ломоносов": {
            "Материалы": "https://olimpiada.ru/activity/348/tasks",
            "Сайт": "https://olymp.msu.ru/rus/event/8514/"
        },
        "Воробьевы горы": {
            "Материалы": "https://olimpiada.ru/activity/115/tasks",
            "Сайт": "https://pvg.mk.ru/"
        },
        "СПбГУ": {
            "Материалы": "https://olympiada.spbu.ru/arkhiv.html",
            "Сайт": "https://olympiada.spbu.ru/predmety/2-uncategorised/4-matematika.html"
        },
    },
    "Программирование": {
        "МОШ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://mos-inf.olimpiada.ru/"
        },
        "ВОШ": {
            "Материалы": "https://olimpiada.ru/activity/73/tasks",
            "Сайт": "https://olympiads.ru/moscow/2023-24/vsosh/index.shtml"
        },
        "Технокубок": {
            "Материалы": "https://olimpiada.ru/activity/5371/tasks",
            "Сайт": "https://techno-cup.ru/"
        },
        "ИТМО": {
            "Материалы": "https://olymp.itmo.ru/p/inf/archive",
            "Сайт": "https://olymp.itmo.ru/p/inf2324/4239"
        },
        "Высшая проба": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it"
        },
        "СПбГУ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://olympiada.spbu.ru/arkhiv.html"
        },
        "Innopolis open": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/"
        },
    },
    "Лингвистика": {
        "ВОШ (Русский)": {
            "Материалы": "https://olimpiada.ru/activity/80/tasks",
            "Сайт": "https://vos.olimpiada.ru/russ/2022_2023"
        },
        "ВОШ (Английский)": {
            "Материалы": "https://olimpiada.ru/activity/88/tasks",
            "Сайт": "https://vos.olimpiada.ru/engl/2022_2023"
        },
        "ВОШ (Китайский)": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://olympiada.spbu.ru/arkhiv.html"
        },
        "МОШ": {
            "Материалы": "https://mos.olimpiada.ru/tasks/ling",
            "Сайт": "https://mos.olimpiada.ru/olymp/ling"
        },
        "Высшая проба (Английский)": {
            "Материалы": "https://olimpiada.ru/activity/5208/tasks",
            "Сайт": "https://olymp.hse.ru/mmo/lang"
        },
        "СПбГУ (Иностранные языки)": {
            "Материалы": "https://olympiada.spbu.ru/arkhiv.html",
            "Сайт": "https://olympiada.spbu.ru/predmety/10-predmety/16-filologiya-kompleks-predmetov-russkij-yazyk-literatura-inostrannyj-yazyk.html"
        }
    },
    "Экономика": {
        "МОШ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://mos-inf.olimpiada.ru/"
        },
        "ВОШ": {
            "Материалы": "https://olimpiada.ru/activity/73/tasks",
            "Сайт": "https://olympiads.ru/moscow/2023-24/vsosh/index.shtml"
        },
        "Высшая проба (Экономика)": {
            "Материалы": "https://olimpiada.ru/activity/5371/tasks",
            "Сайт": "https://techno-cup.ru/"
        },
        "Кондратьев": {
            "Материалы": "https://olymp.itmo.ru/p/inf/archive",
            "Сайт": "https://olymp.itmo.ru/p/inf2324/4239"
        },
        "Финансовый Университет": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it"
        },
        "СПбГУ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://olympiada.spbu.ru/arkhiv.html"
        },
        "Сибириада": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/"
        },
        "Ранхигс": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/"
        },
        "Плехановская": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/"
        },
        "Высшая проба (Финансовая грамотность)": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it"
        },
        "Кейс-чемпионат": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it"
        },
        "Высшая проба (Основы бизнеса)": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it"
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

    #Обработка в меню выбора между преметами

    @client.on(events.CallbackQuery(data=b"/subjects"))
    async def subjects(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Математика", b"/math"), Button.inline("Лингвистика", b"/linguistics")],
            [Button.inline("Информатика", b"/informatics"), Button.inline("Экономика", b"/economics")],
            [Button.inline("Социальные науки", b"/social_studies")]
        ]
        await event.respond("Выберите предмет, об олимпиадах по которому Вы бы хотели узнать:", buttons=buttons)

    @client.on(events.CallbackQuery(data=b"/math"))
    async def math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("ММО", b"/mmo_math"), Button.inline("ВОШ", b"/vosh_math")],
            [Button.inline("Турнир городов", b"/turgor"), Button.inline("Высшая проба", b"/vp_math")],
            [Button.inline("Физтех", b"/mpti_math"), Button.inline("Ломоносов", b"/lomonosov_math")],
            [Button.inline("Воробьевы горы", b"/pvg_math"), Button.inline("СПбГУ", b"/spbu_math")],
        ]
        await event.respond("Математика:", buttons=buttons)
        user_selections[chat_id]["subject"] = "Математика"

    @client.on(events.CallbackQuery(data=b"/linguistics"))
    async def linguistics(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Высшая проба (английский)", b"/linguistics_vp_english"),Button.inline("ВОШ (русский)", b"/linguistics_vosh_russian")],
            [Button.inline("ВОШ (английский)", b"/linguistics_vosh_english"), Button.inline("ВОШ (китайский)", b"/linguistics_vosh_chinese")],
            [Button.inline("МОШ", b"/linguistics_mosh"), Button.inline("СПбГУ (иностранные языки)", b"/spbu_foreign_lang")],       
        ]
        await event.respond("Лингвистика:", buttons=buttons)
        user_selections[chat_id]["subject"] = "Лингвистика"

    @client.on(events.CallbackQuery(data=b"/economics"))
    async def economics(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("МОШ", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")],
            [Button.inline("", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")],
            [Button.inline("МОШ", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")],
            [Button.inline("МОШ", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")],
            [Button.inline("МОШ", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")]
        ]
        await event.respond("Экономика:", buttons=buttons)
        user_selections[chat_id]["subject"] = "Экономика"

    @client.on(events.CallbackQuery(data=b"/informatics"))
    async def informatics(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("МОШ", b"/mosh_info"), Button.inline("ВОШ", b"/vosh_info")],
            [Button.inline("Технокубок", b"/techno_info"), Button.inline("ИТМО", b"/itmo_info")],
            [Button.inline("Высшая проба", b"/vp_info"), Button.inline("СПбГУ", b"/spbu_info")],
            [Button.inline("Innopolis open", b"/innopolis_info")]
        ]
        await event.respond("Информатика:", buttons=buttons)
        user_selections[chat_id]["subject"] = "Информатика"

    @client.on(events.CallbackQuery(data=b"/social_studies"))
    async def social_studies(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("МОШ", b"/mosh"), Button.inline("Всеросс", b"/vseross")]
        ]
        await event.respond("Социальные науки:", buttons=buttons)
        user_selections[chat_id]["subject"] = "Социальные науки"


    #######################################################################################
    # Модуль математических олимпиад
    # При выборе ММО
    @client.on(events.CallbackQuery(data=b"/mmo"))
    async def mmo_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/mmo_math_reminder"), Button.inline("Материалы", b"/mmo_math_materials"), Button.inline("Сайт", b"/mmo_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/mmo_math_info")]
        ]
        await event.respond("ММО:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ММО"

    @client.on(events.CallbackQuery(data=b"/mmo_math_materials"))
    async def mmo_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "ММО" and url:
            await event.respond("Архив заданий ММО", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/mmo_math_site"))
    async def mmo_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/mmo_math_info"))
    async def mmo_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ММО":
            message = "Московская математическая олимпиада (ММО) - это престижное соревнование, проводимое в Москве. "
            message += "Участие в ММО может открыть двери в лучшие образовательные учреждения страны. "
            message += "Для получения подробной информации посетите официальный сайт ММО."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе ВОШ
    @client.on(events.CallbackQuery(data=b"/vosh_math"))
    async def vosh_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/vosh_math_reminder"), Button.inline("Материалы", b"/vosh_math_materials"), Button.inline("Сайт", b"/vosh_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/vosh_math_info")]
        ]
        await event.respond("ВОШ:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ"

    @client.on(events.CallbackQuery(data=b"/vosh_math_materials"))
    async def vosh_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "ВОШ" and url:
            await event.respond("Архив заданий ВОШ", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_math_site"))
    async def vosh_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_math_info"))
    async def vosh_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ":
            message = "Всероссийская олимпиада школьников (ВОШ) - это престижное соревнование, проводимое в несколько этапов. "
            message += "Призерство в ВОШ откроет двери в лучшие образовательные учреждения страны. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Турнира городов
    @client.on(events.CallbackQuery(data=b"/vosh_math"))
    async def vosh_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/vosh_math_reminder"), Button.inline("Материалы", b"/vosh_math_materials"), Button.inline("Сайт", b"/vosh_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/vosh_math_info")]
        ]
        await event.respond("ВОШ:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ"

    @client.on(events.CallbackQuery(data=b"/vosh_math_materials"))
    async def vosh_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "ВОШ" and url:
            await event.respond("Архив заданий ВОШ", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_math_site"))
    async def vosh_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_math_info"))
    async def vosh_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ":
            message = "Всероссийская олимпиада школьников (ВОШ) - это престижное соревнование, проводимое в несколько этапов. "
            message += "Призерство в ВОШ откроет двери в лучшие образовательные учреждения страны. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Высшей пробы
    @client.on(events.CallbackQuery(data=b"/vp_math"))
    async def vp_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/vp_math_reminder"), Button.inline("Материалы", b"/vp_math_materials"), Button.inline("Сайт", b"/vp_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/vp_math_info")]
        ]
        await event.respond("Высшая проба:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Высшая проба"

    @client.on(events.CallbackQuery(data=b"/vp_math_materials"))
    async def vp_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Высшая проба" and url:
            await event.respond("Архив заданий Высшей пробы", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/vp_math_site"))
    async def vp_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/vp_math_info"))
    async def vp_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Высшая проба":
            message = "Высшая проба - это престижное соревнование по математике, охватывающее различные уровни сложности. "
            message += "Для получения подробной информации посетите официальный сайт Высшей пробы."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Физтех
    @client.on(events.CallbackQuery(data=b"/mpti_math"))
    async def mpti_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/mpti_math_reminder"), Button.inline("Материалы", b"/mpti_math_materials"), Button.inline("Сайт", b"/mpti_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/mpti_math_info")]
        ]
        await event.respond("Физтех:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Физтех"

    @client.on(events.CallbackQuery(data=b"/mpti_math_materials"))
    async def mpti_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Физтех" and url:
            await event.respond("Архив заданий Физтеха", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/mpti_math_site"))
    async def mpti_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/mpti_math_info"))
    async def mpti_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Физтех":
            message = "Олимпиада 'Физтех' проводится Физтех-лицеем МФТИ. "
            message += "Для получения подробной информации посетите официальный сайт олимпиады 'Физтех'."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Ломоносов
    @client.on(events.CallbackQuery(data=b"/lomonosov_math"))
    async def lomonosov_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/lomonosov_math_reminder"), Button.inline("Материалы", b"/lomonosov_math_materials"), Button.inline("Сайт", b"/lomonosov_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/lomonosov_math_info")]
        ]
        await event.respond("Ломоносов:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Ломоносов"

    @client.on(events.CallbackQuery(data=b"/lomonosov_math_materials"))
    async def lomonosov_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Ломоносов" and url:
            await event.respond("Архив заданий Ломоносова", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/lomonosov_math_site"))
    async def lomonosov_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/lomonosov_math_info"))
    async def lomonosov_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Ломоносов":
            message = "Олимпиада 'Ломоносов' - это масштабное соревнование для школьников. "
            message += "Для получения подробной информации посетите официальный сайт олимпиады 'Ломоносов'."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Воробьевы горы
    @client.on(events.CallbackQuery(data=b"/pvg_math"))
    async def pvg_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/pvg_math_reminder"), Button.inline("Материалы", b"/pvg_math_materials"), Button.inline("Сайт", b"/pvg_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/pvg_math_info")]
        ]
        await event.respond("Воробьевы горы:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Воробьевы горы"

    @client.on(events.CallbackQuery(data=b"/pvg_math_materials"))
    async def pvg_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Воробьевы горы" and url:
            await event.respond("Архив заданий Воробьевых гор", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/pvg_math_site"))
    async def pvg_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/pvg_math_info"))
    async def pvg_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Воробьевы горы":
            message = "Олимпиада 'Воробьевы горы' - это... (информация о Воробьевых горах)"
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе СПбГУ
    @client.on(events.CallbackQuery(data=b"/spbu_math"))
    async def spbu_math(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/spbu_math_reminder"), Button.inline("Материалы", b"/spbu_math_materials"), Button.inline("Сайт", b"/spbu_math_site")],
            [Button.inline("Факультативы по подготовке", b"/math_electives"), Button.inline("Об олимпиаде", b"/spbu_math_info")]
        ]
        await event.respond("СПБГУ:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "СПБГУ"

    @client.on(events.CallbackQuery(data=b"/spbu_math_materials"))
    async def spbu_math_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "СПБГУ" and url:
            await event.respond("Архив заданий СПБГУ", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/spbu_math_site"))
    async def spbu_math_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/spbu_math_info"))
    async def spbu_math_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "СПБГУ":
            message = "Олимпиада СПБГУ - это... (информация о СПБГУ)"
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # Факультативы по математике

    @client.on(events.CallbackQuery(data=b"/math_electives"))
    async def math_electives(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Понедельник", b"/monday_math"), Button.inline("Вторник", b"/tuesday_math")],
            [Button.inline("Среда", b"/wednesday_math"), Button.inline("Четверг", b"/thursday_math")],
            [Button.inline("Пятница", b"/friday_math"), Button.inline("Суббота", b"/saturday_math")]
        ]
        await event.respond("Дни факультативов, которые могут помочь подготовиться:", buttons=buttons)

    @client.on(events.CallbackQuery(data=b"/monday_math"))
    async def monday_math(event):
        message = '''
    1. "Олимпиадная математика" (для 11М) - ведет Короленков В. А., кабинет С201, 17:05 - 18:30.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/tuesday_math"))
    async def tuesday_math(event):
        message = '''
    1. "Перечневые олимпиады по математике" (для 11) - ведет Акопян А. А., кабинет С201, 16:30 - 18:00.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/wednesday_math"))
    async def wednesday_math(event):
        message = '''
    1. "Планиметрия к ЕГЭ" (для 10-11) - ведет Кучумова Д. А., кабинет С302, 18:00 - 19:25.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/thursday_math"))
    async def thursday_math(event):
        message = '''
    1. "Решение задач по стереометрии и теории чисел для подготовки к ЕГЭ и олимпиадам" (для 10-11) - ведет Уклеин Г. И., кабинет С303, 17:00 - 18:20.
    2. "Решение задач ЕГЭ повышенного уровня сложности" (для 11) - ведет Миткевич И. А., онлайн, 10:00 - 11:30
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/friday_math"))
    async def friday_math(event):
        message = '''
    1. "Перечневые олимпиады по математике" (для 10) - ведет Акопян А. А., кабинет С201, 16:30 - 18:00.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/saturday_math"))
    async def saturday_math(event):
        message = '''
    1. "Олимпиадная математика" (для 11М) - ведет Обухов Б., кабинет С302, 12:20 - 13:45.
    2. "Олимпиадная математика" (для 11М) - ведет Браженко А. С., кабинет С303, 14:45 - 16:10.
    '''
        await event.respond(message)

    #######################################################################################
    #Модуль олимпиад по информатике
    # При выборе МОШ (Информатика)
    @client.on(events.CallbackQuery(data=b"/mosh_info"))
    async def mosh_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/mosh_info_reminder"), Button.inline("Материалы", b"/mosh_info_materials"), Button.inline("Сайт", b"/mosh_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/mosh_info_olympiad_info")]
        ]
        await event.respond("МОШ (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "МОШ"

    @client.on(events.CallbackQuery(data=b"/mosh_info_materials"))
    async def mosh_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "МОШ" and url:
            await event.respond("Архив заданий МОШ (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/mosh_info_site"))
    async def mosh_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт МОШ (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/mosh_info_olympiad_info"))
    async def mosh_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "МОШ":
            message = "Московская олимпиада школьников (МОШ) - это престижное соревнование по информатике. "
            message += "Участие в МОШ может открыть двери в лучшие образовательные учреждения страны. "
            message += "Для получения подробной информации посетите официальный сайт МОШ (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе ВОШ (Информатика)
    @client.on(events.CallbackQuery(data=b"/vosh_info"))
    async def vosh_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/vosh_info_reminder"), Button.inline("Материалы", b"/vosh_info_materials"), Button.inline("Сайт", b"/vosh_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/vosh_info_olympiad_info")]
        ]
        await event.respond("ВОШ (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ"

    @client.on(events.CallbackQuery(data=b"/vosh_info_materials"))
    async def vosh_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "ВОШ" and url:
            await event.respond("Архив заданий ВОШ (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_info_site"))
    async def vosh_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт ВОШ (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/vosh_info_olympiad_info"))
    async def vosh_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ":
            message = "Всероссийская олимпиада школьников (ВОШ) - это престижное соревнование по информатике. "
            message += "Призерство в ВОШ откроет двери в лучшие образовательные учреждения страны. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Технокубка
    @client.on(events.CallbackQuery(data=b"/technocup_info"))
    async def technocup_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/technocup_info_reminder"), Button.inline("Материалы", b"/technocup_info_materials"), Button.inline("Сайт", b"/technocup_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/technocup_info_olympiad_info")]
        ]
        await event.respond("Технокубок (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Технокубок"

    @client.on(events.CallbackQuery(data=b"/technocup_info_materials"))
    async def technocup_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Технокубок" and url:
            await event.respond("Архив заданий Технокубок (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/technocup_info_site"))
    async def technocup_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт Технокубок (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/technocup_info_olympiad_info"))
    async def technocup_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Технокубок":
            message = "Технокубок - это олимпиада по информатике среди школьников. "
            message += "Участие в Технокубок может быть полезным для развития навыков в программировании и информатике. "
            message += "Для получения подробной информации посетите официальный сайт Технокубок (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе ИТМО
    @client.on(events.CallbackQuery(data=b"/itmo_info"))
    async def itmo_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/itmo_info_reminder"), Button.inline("Материалы", b"/itmo_info_materials"), Button.inline("Сайт", b"/itmo_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/itmo_info_olympiad_info")]
        ]
        await event.respond("ИТМО (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ИТМО"

    @client.on(events.CallbackQuery(data=b"/itmo_info_materials"))
    async def itmo_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "ИТМО" and url:
            await event.respond("Архив заданий ИТМО (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/itmo_info_site"))
    async def itmo_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт ИТМО (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/itmo_info_olympiad_info"))
    async def itmo_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ИТМО":
            message = "Олимпиада ИТМО - это соревнование по информатике, проводимое ИТМО. "
            message += "Участие в ИТМО может помочь развить навыки в программировании и информатике. "
            message += "Для получения подробной информации посетите официальный сайт ИТМО (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Высшей пробы(Информатика)
    @client.on(events.CallbackQuery(data=b"/vp_info"))
    async def vp_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/vp_info_reminder"), Button.inline("Материалы", b"/vp_info_materials"), Button.inline("Сайт", b"/vp_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/vp_info_olympiad_info")]
        ]
        await event.respond("Высшая проба (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Высшая проба"

    @client.on(events.CallbackQuery(data=b"/vp_info_materials"))
    async def vp_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Высшая проба" and url:
            await event.respond("Архив заданий Высшая проба (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/vp_info_site"))
    async def vp_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт Высшая проба (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/vp_info_olympiad_info"))
    async def vp_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Высшая проба":
            message = "Высшая проба - это олимпиада по информатике для школьников. "
            message += "Участие в Высшей пробе может помочь развить навыки в программировании и информатике. "
            message += "Для получения подробной информации посетите официальный сайт Высшей пробы (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе СПбГУ(Информатика)
    @client.on(events.CallbackQuery(data=b"/spbu_info"))
    async def spbu_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/spbu_info_reminder"), Button.inline("Материалы", b"/spbu_info_materials"), Button.inline("Сайт", b"/spbu_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/spbu_info_olympiad_info")]
        ]
        await event.respond("СПбГУ (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "СПбГУ"

    @client.on(events.CallbackQuery(data=b"/spbu_info_materials"))
    async def spbu_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "СПбГУ" and url:
            await event.respond("Архив заданий СПбГУ (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/spbu_info_site"))
    async def spbu_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт СПбГУ (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/spbu_info_olympiad_info"))
    async def spbu_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "СПбГУ":
            message = "СПбГУ - это олимпиада по информатике, проводимая в Санкт-Петербургском государственном университете. "
            message += "Участие в этой олимпиаде может помочь развить навыки в программировании и информатике. "
            message += "Для получения подробной информации посетите официальный сайт СПбГУ (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Innopolis open
    @client.on(events.CallbackQuery(data=b"/innopolis_info"))
    async def innopolis_info(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/innopolis_info_reminder"), Button.inline("Материалы", b"/innopolis_info_materials"), Button.inline("Сайт", b"/innopolis_info_site")],
            [Button.inline("Факультативы по подготовке", b"/informatics_electives"), Button.inline("Об олимпиаде", b"/innopolis_info_olympiad_info")]
        ]
        await event.respond("Innopolis open (Информатика):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Innopolis open"

    @client.on(events.CallbackQuery(data=b"/innopolis_info_materials"))
    async def innopolis_info_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if subject_type == "Innopolis open" and url:
            await event.respond("Архив заданий Innopolis open (Информатика)", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Архив не найден")

    @client.on(events.CallbackQuery(data=b"/innopolis_info_site"))
    async def innopolis_info_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт Innopolis open (Информатика)", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/innopolis_info_olympiad_info"))
    async def innopolis_info_olympiad_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Innopolis open":
            message = "Innopolis open - это соревнование по информатике для школьников, проводимое Иннополисом. "
            message += "Участие в Innopolis open может помочь развить навыки в программировании и информатике. "
            message += "Для получения подробной информации посетите официальный сайт Innopolis open (Информатика)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # Факультативы по информатике

    @client.on(events.CallbackQuery(data=b"/informatics_electives"))
    async def informatics_electives(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Понедельник", b"/monday_info"), Button.inline("Вторник", b"/tuesday_info")],
            [Button.inline("Среда", b"/wednesday_info"), Button.inline("Четверг", b"/thursday_info")],
            [Button.inline("Пятница", b"/friday_info"), Button.inline("Суббота", b"/saturday_info")]
        ]
        await event.respond("Дни факультативов, которые могут помочь подготовиться:", buttons=buttons)

    @client.on(events.CallbackQuery(data=b"/monday_info"))
    async def monday_info(event):
        message = '''
    В этот день факультативов по выбранному предмету нет.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/tuesday_info"))
    async def tuesday_info(event):
        message = '''
    1. "Олимпиадное программирование" (для 8-9) - ведет Козлов М. Д., онлайн, 18:00 - 19:30.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/wednesday_info"))
    async def wednesday_info(event):
        message = '''
    1. "Решение задач повышенной сложности в формате ЕГЭ" (для 10-11) - ведет Гасилин М. Д., онлайн, 18:00 - 19:30.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/thursday_info"))
    async def thursday_info(event):
        message = '''
    В этот день факультативов по выбранному предмету нет.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/friday_info"))
    async def friday_info(event):
        message = '''
    В этот день факультативов по выбранному предмету нет.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/saturday_info"))
    async def saturday_info(event):
        message = '''
    1. "Олимпиадное программирование" (для 8-9) - Козлов М. Д., онлайн, 12:00 - 15:00.
    2. "Введение в информационную безопасность" (для 9-11) - ведет Веселов К. А., кабинет С204, 15:30 - 18:30.
    '''
        await event.respond(message)

    #######################################################################################
    #Модуль олимпиад по лингвистике и т.д.
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт Евразийская", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")
    # При выборе ВОШ (русский)
    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_russian"))
    async def linguistics_vosh_russian(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_vosh_russian_reminder"), Button.inline("Материалы", b"/linguistics_vosh_russian_materials"), Button.inline("Сайт", b"/linguistics_vosh_russian_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/linguistics_vosh_russian_info")]
        ]
        await event.respond("ВОШ (русский):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ (русский)"

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_russian_materials"))
    async def linguistics_vosh_russian_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы ВОШ (русский):", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_russian_site"))
    async def linguistics_vosh_russian_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
        if url:
            await event.respond(f"Официальный сайт ВОШ (русский):", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_russian_info"))
    async def linguistics_vosh_russian_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ (русский)":
            message = "Всероссийская олимпиада школьников (ВОШ) проводит соревнования в области лингвистики, включая русский язык. "
            message += "Участие в ВОШ позволяет школьникам продемонстрировать свои знания в лингвистической области. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ (русский)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе ВОШ (английский)
    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_english"))
    async def linguistics_vosh_english(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_vosh_english_reminder"), Button.inline("Материалы", b"/linguistics_vosh_english_materials"), Button.inline("Сайт", b"/linguistics_vosh_english_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/linguistics_vosh_english_info")]
        ]
        await event.respond("ВОШ (английский):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ (английский)"

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_english_materials"))
    async def linguistics_vosh_english_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы ВОШ (английский):", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_english_site"))
    async def linguistics_vosh_english_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
        if url:
            await event.respond(f"Официальный сайт ВОШ (английский):", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_english_info"))
    async def linguistics_vosh_english_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ (английский)":
            message = "Всероссийская олимпиада школьников (ВОШ) проводит соревнования в области лингвистики, включая английский язык. "
            message += "Участие в ВОШ позволяет школьникам продемонстрировать свои знания в английском языке. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ (английский)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе ВОШ (китайский)
    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_chinese"))
    async def linguistics_vosh_chinese(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_vosh_chinese"), Button.inline("Материалы", b"/linguistics_vosh_chinese_materials"), Button.inline("Сайт", b"/linguistics_vosh_chinese_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/linguistics_vosh_chinese_info")]
        ]
        await event.respond("ВОШ (китайский):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "ВОШ (китайский)"

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_chinese_materials"))
    async def linguistics_vosh_chinese_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы ВОШ (китайский):", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_chinese_site"))
    async def linguistics_vosh_chinese_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
        if url:
            await event.respond(f"Официальный сайт ВОШ (китайский):", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/linguistics_vosh_chinese_info"))
    async def linguistics_vosh_chinese_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "ВОШ (китайский)":
            message = "Всероссийская олимпиада школьников (ВОШ) проводит соревнования в области китайского языка. "
            message += "Участие в ВОШ (китайский) позволяет школьникам продемонстрировать свои знания в китайском языке. "
            message += "Для получения подробной информации посетите официальный сайт ВОШ (китайский)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе МОШ
    @client.on(events.CallbackQuery(data=b"/linguistics_mosh"))
    async def linguistics_mosh(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_mosh"), Button.inline("Материалы", b"/linguistics_mosh_materials"), Button.inline("Сайт", b"/linguistics_mosh_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/linguistics_mosh_info")]
        ]
        await event.respond("МОШ:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "МОШ"

    @client.on(events.CallbackQuery(data=b"/linguistics_mosh_materials"))
    async def linguistics_mosh_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы МОШ:", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/linguistics_mosh_site"))
    async def linguistics_mosh_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")

        if url:
            await event.respond(f"Официальный сайт МОШ:", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/linguistics_mosh_info"))
    async def linguistics_mosh_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "МОШ":
            message = "Московская олимпиада школьников (МОШ) проводит соревнования в области лингвистики. "
            message += "Участие в МОШ позволяет школьникам проявить свои знания в языках и лингвистических науках. "
            message += "Для получения подробной информации посетите официальный сайт МОШ."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе Высшей пробы (английский)
    @client.on(events.CallbackQuery(data=b"/linguistics_vp_english"))
    async def linguistics_vp_english(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_vp_english"), Button.inline("Материалы", b"/linguistics_vp_english_materials"), Button.inline("Сайт", b"/linguistics_vp_english_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/linguistics_vp_english_info")]
        ]
        await event.respond("Высшая проба (английский):", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Высшая проба (английский)"

    @client.on(events.CallbackQuery(data=b"/linguistics_vp_english_materials"))
    async def linguistics_vp_english_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы Высшей пробы (английский):", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/linguistics_vp_english_site"))
    async def linguistics_vp_english_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
        if url:
            await event.respond(f"Официальный сайт Высшей пробы (английский):", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/linguistics_vp_english_info"))
    async def linguistics_vp_english_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
                
        if subject_type == "Высшая проба (английский)":
            message = "Высшая проба - это олимпиада по английскому языку для школьников. "
            message += "Участие в ней позволяет школьникам продемонстрировать свои навыки в английском языке и лингвистике. "
            message += "Для получения подробной информации посетите официальный сайт Высшей пробы (английский)."
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."

        await event.respond(message)


    # При выборе СПбГУ (иностранный язык)
    @client.on(events.CallbackQuery(data=b"/spbu_foreign_lang"))
    async def spbu_foreign_lang(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Напоминание", b"/linguistics_spbu_foreign_lang"), Button.inline("Материалы", b"/spbu_foreign_lang_materials"), Button.inline("Сайт", b"/spbu_foreign_lang_site")],
            [Button.inline("Факультативы по подготовке", b"/linguistics_electives"), Button.inline("Информация", b"/spbu_foreign_lang_info")]
        ]
        await event.respond("Новая олимпиада:", buttons=buttons)
        user_selections[chat_id]["subject_type"] = "Новая олимпиада"

    @client.on(events.CallbackQuery(data=b"/spbu_foreign_lang_materials"))
    async def spbu_foreign_lang_materials(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
        if url:
            await event.respond("Материалы Новой олимпиады:", buttons=[Button.url("Материалы", url)])
        else:
            await event.respond("Материалы не найдены")

    @client.on(events.CallbackQuery(data=b"/spbu_foreign_lang_site"))
    async def spbu_foreign_lang_site(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        subject = user_selections.get(chat_id, {}).get("subject")
        url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
        if url:
            await event.respond(f"Официальный сайт Новой олимпиады:", buttons=[Button.url("Сайт", url)])
        else:
            await event.respond("Сайт не найден")

    @client.on(events.CallbackQuery(data=b"/spbu_foreign_lang_info"))
    async def spbu_foreign_lang_info(event):
        chat_id = event.chat_id
        subject_type = user_selections.get(chat_id, {}).get("subject_type")
        if subject_type == "Новая олимпиада":
            message = "Информация о Новой олимпиаде:\n\n"
            message += "Это новая олимпиада. Это информация о ней."
            await event.respond(message)
        else:
            message = "Информация об олимпиаде не доступна. Пожалуйста, выберите предмет и тип олимпиады."
            await event.respond(message)


    # Факультативы по лингвистике
    @client.on(events.CallbackQuery(data=b"/linguistics_electives"))
    async def linguistics_electives(event):
        chat_id = event.chat_id
        buttons = [
            [Button.inline("Понедельник", b"/monday_linguistics"), Button.inline("Вторник", b"/tuesday_linguistics")],
            [Button.inline("Среда", b"/wednesday_linguistics"), Button.inline("Четверг", b"/thursday_linguistics")],
            [Button.inline("Пятница", b"/friday_linguistics"), Button.inline("Суббота", b"/saturday_linguistics")]
        ]
        await event.respond("Дни факультативов, которые могут помочь подготовиться:", buttons=buttons)

    @client.on(events.CallbackQuery(data=b"/monday_linguistics"))
    async def monday_linguistics(event):
        message = '''
    1. "Подготовка к олимпиаде Высшая проба по английскому языку" (для 10-11) - ведет Воронкова А. В., Актовый зал Колобок, 16:40 - 18:50.
    2. "Подготовка к олимпиаде Высшая проба по английскому языку" (для 10-11) - ведет Глазкова А. М., БХ510, 16:40 - 18:50.
    3. "Олимпиадный курс по английскому языку" (для 9-11) - ведет Михайлова Е.В., С409, 17:00 - 18:30.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/tuesday_linguistics"))
    async def tuesday_linguistics(event):
        message = '''
    1. "Олимпиадный курс по английскому языку" (для 8) - ведет Ординарцева А.А., Л307, 16:30 - 17:55.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/wednesday_linguistics"))
    async def wednesday_linguistics(event):
        message = '''
    В этот день факультативов по выбранному предмету нет.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/thursday_linguistics"))
    async def thursday_linguistics(event):
        message = '''
    1. "Китайский разговорный тандем-клуб" (для 8-11)- ведет Пересадько Т. В., онлайн, 16:20 - 18:30.
    2. "Олимпиадный курс по английскому языку" (для 8) - ведет Ординарцева А.А., Л307, 16:30 - 17:55.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/friday_linguistics"))
    async def friday_linguistics(event):
        message = '''
    3. "Олимпиадный курс по английскому языку" (для 9-11) - ведет Михайлова Е.В., онлайн, 17:00 - 18:30.
    '''
        await event.respond(message)

    @client.on(events.CallbackQuery(data=b"/saturday_linguistics"))
    async def saturday_linguistics(event):
        message = '''
    1. "Китайский для начинающих" (для 8-11)- ведет Пересадько Т. В., онлайн, 16:20 - 18:30.
    2. "Продвинутый китайский " (для 8-11)- ведет Пересадько Т. В., онлайн, 14:00 - 16:10.
    '''
        await event.respond(message)


    #######################################################################################
    #Модуль олимпиад по экономике
        print("Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())