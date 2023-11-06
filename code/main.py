from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button


api_id = 26730332
api_hash = '444cac746aea62c94690b4217f412c9e'
bot_token = '6643259676:AAHuAQXWS4dZZSV17ql6vP2v19cxaBpWMbc'


# Словарь для отслеживания пользователей, которые начали разговор
started_conversations = {}

# Словарь для хранения выбора пользователей
user_selections = {}

# Словарь для хранения ссылок
urls = {
    "Математика": {
        "ММО": {
            "Материалы": "https://mos.olimpiada.ru/tasks/math",
            "Сайт": "https://mmo.mccme.ru/",
            "Информация": ("Московская Математическая Олимпиада (ММО) - олимпиада по математике, имеющая первый уровень, что может дать БВИ или полные 100 баллов, во многие ВУЗы."
                           "Состоит из 2 этапов: Отборочный, Заключительный. Больше можно узнать на сайте или в материалах.")
        },
        "ВОШ": {
            "Материалы": "https://olimpiada.ru/activity/72/tasks",
            "Сайт": "https://vos.olimpiada.ru/math/2023_2024",
        },
        "Турнир городов": {
            "Материалы": "https://www.turgor.ru/problems/",
            "Сайт": "https://www.turgor.ru/",
        },
        "Высшая проба": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-math",
            "Сайт": "https://olymp.hse.ru/mmo/math",
        },
        "Физтех": {
            "Материалы": "https://olymp.mipt.ru/olympiad/samples",
            "Сайт": "https://olymp-online.mipt.ru/",
        },
        "Ломоносов": {
            "Материалы": "https://olimpiada.ru/activity/348/tasks",
            "Сайт": "https://olymp.msu.ru/rus/event/8514/",
        },
        "Воробьевы горы": {
            "Материалы": "https://olimpiada.ru/activity/115/tasks",
            "Сайт": "https://pvg.mk.ru/",
        },
        "СПбГУ": {
            "Материалы": "https://olympiada.spbu.ru/arkhiv.html",
            "Сайт": "https://olympiada.spbu.ru/predmety/2-uncategorised/4-matematika.html",
        },
    },
    "Экономика": {
        "МОШ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://mos-inf.olimpiada.ru/",
        },
        "ВОШ": {
            "Материалы": "https://olimpiada.ru/activity/73/tasks",
            "Сайт": "https://olympiads.ru/moscow/2023-24/vsosh/index.shtml",
        },
        "Высшая проба (Экономика)": {
            "Материалы": "https://olimpiada.ru/activity/5371/tasks",
            "Сайт": "https://techno-cup.ru/",
        },
        "Кондратьев": {
            "Материалы": "https://olymp.itmo.ru/p/inf/archive",
            "Сайт": "https://olymp.itmo.ru/p/inf2324/4239",
        },
        "Финансовый Университет": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it",
        },
        "СПбГУ": {
            "Материалы": "https://mos-inf.olimpiada.ru/mosh_past",
            "Сайт": "https://olympiada.spbu.ru/arkhiv.html",
        },
        "Сибириада": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/",
        },
        "Ранхигс": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/",
        },
        "Плехановская": {
            "Материалы": "https://olymp.innopolis.university/",
            "Сайт": "https://olymp.innopolis.ru/ooui/informatics/archive/",
        },
        "Высшая проба (Финансовая грамотность)": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it",
        },
        "Кейс-чемпионат": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it",
        },
        "Высшая проба (Основы бизнеса)": {
            "Материалы": "https://olymp.hse.ru/mmo/tasks-it",
            "Сайт": "https://olymp.hse.ru/mmo/it",
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
        [Button.inline("Выбор олимпиад", b"/subjects"), Button.inline("Закончить диалог", b"/end")]
    ]
    return message, buttons


if __name__ == '__main__':
    import asyncio

    async def run_bot():
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

            @client.on(events.CallbackQuery(data=b"/subjects"))
            async def subjects(event):
                chat_id = event.chat_id
                buttons = [
                    [Button.inline("Математика", b"/math"), Button.inline("Экономика", b"/economics")],
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
                    [Button.inline("В меню", b"/subjects")]
                ]
                await event.respond("Математика:", buttons=buttons)
                user_selections[chat_id]["subject"] = "Математика"

            @client.on(events.CallbackQuery(data=b"/economics"))
            async def economics(event):
                chat_id = event.chat_id
                buttons = [
                    [Button.inline("МОШ", b"/mosh_econ"), Button.inline("ВОШ", b"/vosh_econ")],
                    [Button.inline("Высшая проба (Экономика)", b"/vp_econ"), Button.inline("Кондратьев", b"/condratyev")],
                    [Button.inline("Финансовый Университет", b"/finan_uni"), Button.inline("СПбГУ", b"/spbu_econ")],
                    [Button.inline("Сибириада", b"/sibiriada"), Button.inline("РАНХиГС", b"/ranepa")],
                    [Button.inline("Плехановская", b"/plehanov"), Button.inline("Высшая проба (Финансовая грамотность)", b"/vp_finan")],
                    [Button.inline("Кейс-чемпионат", b"/case-champ"), Button.inline("Высшая проба (Основы бизнеса)", b"/vp_business")],
                    [Button.inline("В меню", b"/subjects")]
                ]
                await event.respond("Экономика:", buttons=buttons)
                user_selections[chat_id]["subject"] = "Экономика"


            subject_type_mapping = {
                "vp_math": "Высшая проба",
                "mpti_math": "Физтех",
                "lomonosov_math": "Ломоносов",
                "pvg_math": "Воробьевы горы",
                "spbu_math": "СПБГУ",
                "mmo_math": "ММО",
                "vosh_math": "ВОШ",
                "turgor": "Турнир городов"
            }


#Получение олимпиады
            @client.on(events.CallbackQuery(data=b"/vp_math"))
            async def vp_math(event):
                await handle_math(event, "vp_math")

            @client.on(events.CallbackQuery(data=b"/mpti_math"))
            async def mpti_math(event):
                await handle_math(event, "mpti_math")

            @client.on(events.CallbackQuery(data=b"/lomonosov_math"))
            async def lomonosov_math(event):
                await handle_math(event, "lomonosov_math")

            @client.on(events.CallbackQuery(data=b"/pvg_math"))
            async def pvg_math(event):
                await handle_math(event, "pvg_math")

            @client.on(events.CallbackQuery(data=b"/spbu_math"))
            async def spbu_math(event):
                await handle_math(event, "spbu_math")
            
            @client.on(events.CallbackQuery(data=b"/turgor"))
            async def turgor(event):
                await handle_math(event, "turgor")

            @client.on(events.CallbackQuery(data=b"/mmo_math"))
            async def mmo_math(event):
                await handle_math(event, "mmo_math")

            @client.on(events.CallbackQuery(data=b"/vosh_math"))
            async def vosh_math(event):
                await handle_math(event, "vosh_math")


            async def handle_math(event, data):
                chat_id = event.chat_id
                subject_type = subject_type_mapping.get(data)  # Получаем текстовое название из словаря

                buttons = [
                    [Button.inline("Материалы", f"/{data}_materials"), Button.inline("Сайт", f"/{data}_site")],
                    [Button.inline("Факультативы по подготовке", "/math_electives"), Button.inline("Об олимпиаде", f"/{data}_info")],
                    [Button.inline("В меню", b"/subjects")]
                ]
                await event.respond(f"Вот что я нашел по олимпиаде {subject_type}:", buttons=buttons)


# Кнопка материалов, архивов
            @client.on(events.CallbackQuery(data=b"/vp_math_materials"))
            async def vp_math_materials(event):
                await handle_math_materials(event, "vp_math")

            @client.on(events.CallbackQuery(data=b"/mpti_math_materials"))
            async def mpti_math_materials(event):
                await handle_math_materials(event, "mpti_math")

            @client.on(events.CallbackQuery(data=b"/lomonosov_math_materials"))
            async def lomonosov_math_materials(event):
                await handle_math_materials(event, "lomonosov_math")

            @client.on(events.CallbackQuery(data=b"/pvg_math_materials"))
            async def pvg_math_materials(event):
                await handle_math_materials(event, "pvg_math")

            @client.on(events.CallbackQuery(data=b"/spbu_math_materials"))
            async def spbu_math_materials(event):
                await handle_math_materials(event, "spbu_math")
            
            @client.on(events.CallbackQuery(data=b"/turgor_materials"))
            async def turgor_materials(event):
                await handle_math_materials(event, "turgor_math")

            @client.on(events.CallbackQuery(data=b"/mmo_math_materials"))
            async def mmo_math_materials(event):
                await handle_math_materials(event, "mmo_math")

            @client.on(events.CallbackQuery(data=b"/vosh_math_materials"))
            async def vosh_math_materials(event):
                await handle_math_materials(event, "vosh_math")


            async def handle_math_materials(event, data):
                chat_id = event.chat_id
                subject = "Математика"
                subject_type = subject_type_mapping.get(data)
                url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
                if url:
                    await event.respond(f"Архив заданий {subject_type}", buttons=[Button.url("Материалы", url)])
                else:
                    await event.respond("Архив не найден")


# Кнопка сайта
            @client.on(events.CallbackQuery(data=b"/vp_math_site"))
            async def vp_math_site(event):
                await handle_math_site(event, "vp_math")

            @client.on(events.CallbackQuery(data=b"/mpti_math_site"))
            async def mpti_math_site(event):
                await handle_math_site(event, "mpti_math")

            @client.on(events.CallbackQuery(data=b"/lomonosov_math_site"))
            async def lomonosov_math_site(event):
                await handle_math_site(event, "lomonosov_math")

            @client.on(events.CallbackQuery(data=b"/pvg_math_site"))
            async def pvg_math_site(event):
                await handle_math_site(event, "pvg_math")

            @client.on(events.CallbackQuery(data=b"/spbu_math_site"))
            async def spbu_math_site(event):
                await handle_math_site(event, "spbu_math")
            
            @client.on(events.CallbackQuery(data=b"/turgor_site"))
            async def turgor_site(event):
                await handle_math_site(event, "turgor_math")

            @client.on(events.CallbackQuery(data=b"/mmo_math_site"))
            async def mmo_math_site(event):
                await handle_math_site(event, "mmo_math")

            @client.on(events.CallbackQuery(data=b"/vosh_math_site"))
            async def vosh_math_site(event):
                await handle_math_site(event, "vosh_math")


            async def handle_math_site(event, data):
                chat_id = event.chat_id
                subject = "Математика"
                subject_type = subject_type_mapping.get(data)
                url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
                if url:
                    await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
                else:
                    await event.respond("Сайт не найден")


# Кнопка информации
            @client.on(events.CallbackQuery(data=b"/vp_math_info"))
            async def vp_math_info(event):
                await handle_math_info(event, "vp_math")

            @client.on(events.CallbackQuery(data=b"/mpti_math_info"))
            async def mpti_math_info(event):
                await handle_math_info(event, "mpti_math")

            @client.on(events.CallbackQuery(data=b"/lomonosov_math_info"))
            async def lomonosov_math_info(event):
                await handle_math_info(event, "lomonosov_math")

            @client.on(events.CallbackQuery(data=b"/pvg_math_info"))
            async def pvg_math_info(event):
                await handle_math_info(event, "pvg_math")

            @client.on(events.CallbackQuery(data=b"/spbu_math_info"))
            async def spbu_math_info(event):
                await handle_math_info(event, "spbu_math")

            @client.on(events.CallbackQuery(data=b"/turgor_info"))
            async def turgor_info(event):
                await handle_math_info(event, "turgor_math")

            @client.on(events.CallbackQuery(data=b"/mmo_math_info"))
            async def mmo_math_info(event):
                await handle_math_info(event, "mmo_math")

            @client.on(events.CallbackQuery(data=b"/vosh_math_info"))
            async def vosh_math_info(event):
                await handle_math_info(event, "vosh_math")


            async def handle_math_info(event, data):
                chat_id = event.chat_id
                subject = "Математика"
                subject_type = subject_type_mapping.get(data)
                message = urls.get(subject, {}).get(subject_type, {}).get("Информация")
                if message:
                    await event.respond(message)
                else:
                    await event.respond("Информации по данной олимпиаде нет")


# Факультативы по математике

            @client.on(events.CallbackQuery(data=b"/math_electives"))
            async def math_electives(event):
                chat_id = event.chat_id
                buttons = [
                    [Button.inline("Понедельник", b"/monday_math"), Button.inline("Вторник", b"/tuesday_math")],
                    [Button.inline("Среда", b"/wednesday_math"), Button.inline("Четверг", b"/thursday_math")],
                    [Button.inline("Пятница", b"/friday_math"), Button.inline("Суббота", b"/saturday_math")],
                    [Button.inline("В меню", b"/subjects")]
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


            # Аналогично для экономики

            econ_subject_type_mapping = {
                "vp_econ": "Высшая проба (Экономика)",
                "mosh_econ": "МОШ",
                "vosh_econ": "ВОШ",
                "condratyev": "Кондратьев",
                "finan_uni": "Финансовый Университет",
                "spbu_econ": "СПбГУ",
                "sibiriada": "Сибириада",
                "ranepa": "РАНХиГС",
                "plehanov": "Плехановская",
                "vp_finan": "Высшая проба (Финансовая грамотность)",
                "case-champ": "Кейс-чемпионат",
                "vp_business": "Высшая проба (Основы бизнеса)"
            }

            @client.on(events.CallbackQuery(data=b"/vp_econ"))
            async def vp_econ(event):
                await handle_economics(event, "vp_econ")

            @client.on(events.CallbackQuery(data=b"/mosh_econ"))
            async def mosh_econ(event):
                await handle_economics(event, "mosh_econ")

            @client.on(events.CallbackQuery(data=b"/vosh_econ"))
            async def vosh_econ(event):
                await handle_economics(event, "vosh_econ")
            
            @client.on(events.CallbackQuery(data=b"/condratyev"))
            async def condratyev(event):
                await handle_economics(event, "condratyev")

            @client.on(events.CallbackQuery(data=b"/finan_uni"))
            async def finan_uni(event):
                await handle_economics(event, "finan_uni")

            @client.on(events.CallbackQuery(data=b"/spbu_econ"))
            async def spbu_econ(event):
                await handle_economics(event, "spbu_econ")

            @client.on(events.CallbackQuery(data=b"/sibiriada"))
            async def sibiriada(event):
                await handle_economics(event, "sibiriada")

            @client.on(events.CallbackQuery(data=b"/ranepa"))
            async def ranepa(event):
                await handle_economics(event, "ranepa")

            @client.on(events.CallbackQuery(data=b"/plehanov"))
            async def plehanov(event):
                await handle_economics(event, "plehanov")

            @client.on(events.CallbackQuery(data=b"/vp_finan"))
            async def vp_finan(event):
                await handle_economics(event, "vp_finan")

            @client.on(events.CallbackQuery(data=b"/case-champ"))
            async def case_champ(event):
                await handle_economics(event, "case-champ")

            @client.on(events.CallbackQuery(data=b"/vp_business"))
            async def vp_business(event):
                await handle_economics(event, "vp_business")


            async def handle_economics(event, data):
                chat_id = event.chat_id
                subject_type = econ_subject_type_mapping.get(data)  # Получаем текстовое название из словаря

                buttons = [
                    [Button.inline("Материалы", f"/{data}_materials"), Button.inline("Сайт", f"/{data}_site")],
                    [Button.inline("Факультативы по подготовке", "/econ_electives"), Button.inline("Об олимпиаде", f"/{data}_info")],
                    [Button.inline("В меню", b"/subjects")]
                ]
                await event.respond(f"Вот что я нашел по олимпиаде {subject_type}:", buttons=buttons)
            

            @client.on(events.CallbackQuery(data=b"/vp_econ_materials"))
            async def vp_econ_materials(event):
                await handle_economics_materials(event, "vp_econ")

            @client.on(events.CallbackQuery(data=b"/mosh_econ_materials"))
            async def mosh_econ_materials(event):
                await handle_economics_materials(event, "mosh_econ")

            @client.on(events.CallbackQuery(data=b"/vosh_econ_materials"))
            async def vosh_econ_materials(event):
                await handle_economics_materials(event, "vosh_econ")

            @client.on(events.CallbackQuery(data=b"/condratyev_materials"))
            async def condratyev_materials(event):
                await handle_economics_materials(event, "condratyev")

            @client.on(events.CallbackQuery(data=b"/finan_uni_materials"))
            async def finan_uni_materials(event):
                await handle_economics_materials(event, "finan_uni")

            @client.on(events.CallbackQuery(data=b"/spbu_econ_materials"))
            async def spbu_econ_materials(event):
                await handle_economics_materials(event, "spbu_econ")

            @client.on(events.CallbackQuery(data=b"/sibiriada_materials"))
            async def sibiriada_materials(event):
                await handle_economics_materials(event, "sibiriada")

            @client.on(events.CallbackQuery(data=b"/ranepa_materials"))
            async def ranepa_materials(event):
                await handle_economics_materials(event, "ranepa")

            @client.on(events.CallbackQuery(data=b"/plehanov_materials"))
            async def plehanov_materials(event):
                await handle_economics_materials(event, "plehanov")

            @client.on(events.CallbackQuery(data=b"/vp_finan_materials"))
            async def vp_finan_materials(event):
                await handle_economics_materials(event, "vp_finan")

            @client.on(events.CallbackQuery(data=b"/case-champ_materials"))
            async def case_champ_materials(event):
                await handle_economics_materials(event, "case-champ")

            @client.on(events.CallbackQuery(data=b"/vp_business_materials"))
            async def vp_business_materials(event):
                await handle_economics_materials(event, "vp_business")


            async def handle_economics_materials(event, data):
                chat_id = event.chat_id
                subject = "Экономика"
                subject_type = econ_subject_type_mapping.get(data)
                url = urls.get(subject, {}).get(subject_type, {}).get("Материалы")
                if url:
                    await event.respond(f"Архив заданий {subject_type}", buttons=[Button.url("Материалы", url)])
                else:
                    await event.respond("Архив не найден")
            

            @client.on(events.CallbackQuery(data=b"/vp_econ_site"))
            async def vp_econ_site(event):
                await handle_economics_site(event, "vp_econ")

            @client.on(events.CallbackQuery(data=b"/mosh_econ_site"))
            async def mosh_econ_site(event):
                await handle_economics_site(event, "mosh_econ")

            @client.on(events.CallbackQuery(data=b"/vosh_econ_site"))
            async def vosh_econ_site(event):
                await handle_economics_site(event, "vosh_econ")

            @client.on(events.CallbackQuery(data=b"/condratyev_site"))
            async def condratyev_site(event):
                await handle_economics_site(event, "condratyev")

            @client.on(events.CallbackQuery(data=b"/finan_uni_site"))
            async def finan_uni_site(event):
                await handle_economics_site(event, "finan_uni")

            @client.on(events.CallbackQuery(data=b"/spbu_econ_site"))
            async def spbu_econ_site(event):
                await handle_economics_site(event, "spbu_econ")

            @client.on(events.CallbackQuery(data=b"/sibiriada_site"))
            async def sibiriada_site(event):
                await handle_economics_site(event, "sibiriada")

            @client.on(events.CallbackQuery(data=b"/ranepa_site"))
            async def ranepa_site(event):
                await handle_economics_site(event, "ranepa")

            @client.on(events.CallbackQuery(data=b"/plehanov_site"))
            async def plehanov_site(event):
                await handle_economics_site(event, "plehanov")

            @client.on(events.CallbackQuery(data=b"/vp_finan_site"))
            async def vp_finan_site(event):
                await handle_economics_site(event, "vp_finan")

            @client.on(events.CallbackQuery(data=b"/case-champ_site"))
            async def case_champ_site(event):
                await handle_economics_site(event, "case-champ")

            @client.on(events.CallbackQuery(data=b"/vp_business_site"))
            async def vp_business_site(event):
                await handle_economics_site(event, "vp_business")


            async def handle_economics_site(event, data):
                chat_id = event.chat_id
                subject = "Экономика"
                subject_type = econ_subject_type_mapping.get(data)
                url = urls.get(subject, {}).get(subject_type, {}).get("Сайт")
                if url:
                    await event.respond(f"Официальный сайт {subject_type}", buttons=[Button.url("Сайт", url)])
                else:
                    await event.respond("Сайт не найден")


            @client.on(events.CallbackQuery(data=b"/vp_econ_info"))
            async def vp_econ_info(event):
                await handle_economics_info(event, "vp_econ")

            @client.on(events.CallbackQuery(data=b"/mosh_econ_info"))
            async def mosh_econ_info(event):
                await handle_economics_info(event, "mosh_econ")

            @client.on(events.CallbackQuery(data=b"/vosh_econ_info"))
            async def vosh_econ_info(event):
                await handle_economics_info(event, "vosh_econ")

            @client.on(events.CallbackQuery(data=b"/condratyev_info"))
            async def condratyev_info(event):
                await handle_economics_info(event, "condratyev")

            @client.on(events.CallbackQuery(data=b"/finan_uni_info"))
            async def finan_uni_info(event):
                await handle_economics_info(event, "finan_uni")

            @client.on(events.CallbackQuery(data=b"/spbu_econ_info"))
            async def spbu_econ_info(event):
                await handle_economics_info(event, "spbu_econ")

            @client.on(events.CallbackQuery(data=b"/sibiriada_info"))
            async def sibiriada_info(event):
                await handle_economics_info(event, "sibiriada")

            @client.on(events.CallbackQuery(data=b"/ranepa_info"))
            async def ranepa_info(event):
                await handle_economics_info(event, "ranepa")

            @client.on(events.CallbackQuery(data=b"/plehanov_info"))
            async def plehanov_info(event):
                await handle_economics_info(event, "plehanov")

            @client.on(events.CallbackQuery(data=b"/vp_finan_info"))
            async def vp_finan_info(event):
                await handle_economics_info(event, "vp_finan")

            @client.on(events.CallbackQuery(data=b"/case-champ_info"))
            async def case_champ_info(event):
                await handle_economics_info(event, "case-champ")

            @client.on(events.CallbackQuery(data=b"/vp_business_info"))
            async def vp_business_info(event):
                await handle_economics_info(event, "vp_business")

            async def handle_economics_info(event, data):
                chat_id = event.chat_id
                subject = "Экономика"
                subject_type = econ_subject_type_mapping.get(data)
                message = urls.get(subject, {}).get(subject_type, {}).get("Информация")
                if message:
                    await event.respond(message)
                else:
                    await event.respond("Информации по данной олимпиаде нет")


            # Факультативы по экономике

            @client.on(events.CallbackQuery(data=b"/econ_electives"))
            async def econ_electives(event):
                chat_id = event.chat_id
                buttons = [
                    [Button.inline("Понедельник", b"/monday_econ"), Button.inline("Вторник", b"/tuesday_econ")],
                    [Button.inline("Среда", b"/wednesday_econ"), Button.inline("Четверг", b"/thursday_econ")],
                    [Button.inline("Пятница", b"/friday_econ"), Button.inline("Суббота", b"/saturday_econ")],
                    [Button.inline("В меню", b"/subjects")]
                ]
                await event.respond("Дни факультативов, которые могут помочь подготовиться:", buttons=buttons)

            @client.on(events.CallbackQuery(data=b"/monday_econ"))
            async def monday_econ(event):
                message = '''
            1. "Финансовая грамотность и инвестиции" (для 9-11) - ведут Малый Алексей Денисович и Климентьев Кирилл Станиславович, кабинет К312, 16:30 - 19:30.
            2. "Олимпиадная экономика" (для 10) - ведет Мельников Виктор Александрович, Лицейский клуб Колобок, 17:45 - 19:45.
            '''
                await event.respond(message)

            @client.on(events.CallbackQuery(data=b"/tuesday_econ"))
            async def tuesday_econ(event):
                message = '''
            1. "Олимпиадная экономика" (для 10) - ведет Мельников Виктор Александрович, Актовый зал Колобок, 17:45 - 19:45.
            '''
                await event.respond(message)

            @client.on(events.CallbackQuery(data=b"/wednesday_econ"))
            async def wednesday_econ(event):
                message = '''
            1. "Экономическое-олимпиадное безобразие" (для 8-10) - ведет Золотова Елена Вячеславовна, онлайн, 16:20 - 19:20.
            2. "Олимпиадная экономика" (для 10-11) - ведет Малый Алексей Денисович, К312, 16:30 - 19:40.
            3. "Олимпиадная экономика" (для 9-10) - ведет Михайлов Дмитрий Андреевич, Актовый зал Колобок, 17:10 - 19:30.
            '''
                await event.respond(message)

            @client.on(events.CallbackQuery(data=b"/thursday_econ"))
            async def thursday_econ(event):
                message = '''
            1. "Олимпиадная экономика" (для 11) - ведет Челеховский Александр Николаевич, Лицейский клуб Колобок, 12:30 - 15:30.
            2. "Экономика никому ничего не должна" (для 8-9) - ведет Зенгер Максим Алексеевич, Л105, 16:30 - 18:10
            '''
                await event.respond(message)

            @client.on(events.CallbackQuery(data=b"/friday_econ"))
            async def friday_econ(event):
                message = '''
            1. "Маркетинговые стратегии и технологии построения успешного бизнеса: от исследований до управления проектами" (для 9-11) - ведет Тюрин Дмитрий Валерьевич, онлайн, 17:50 - 20:50.
            '''
                await event.respond(message)

            @client.on(events.CallbackQuery(data=b"/saturday_econ"))
            async def saturday_econ(event):
                message = '''
            1. "Олимпиадная экономика" (для 9) - ведут Челеховский Александр Николаевич и Бахтимова Вера Анатольевна, Актовый зал Колобок, 10:40 - 13:40.
            2. "Олимпиадная экономика" (для 11) - ведет Челеховский Александр Николаевич, Лицейский клуб Колобок, 14:30 - 17:30.
            3. "Решение олимпиадных заданий по экономике" (для 10) - ведет Бахтимова Вера Анатольевна, кабинет К110, 14:45 - 17:45.
            4. "Олимпиадная экономика" (для 9-10) - ведет Михайлов Дмитрий Андреевич, Актовый зал, 15:20 - 17:30.
            '''
                await event.respond(message)

            print("Бот запущен. Нажмите Ctrl+C, чтобы остановить.")
            await client.run_until_disconnected()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
