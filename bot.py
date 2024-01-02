#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
2023-12-25 Fil - Future code Yandex.Practicum
Многопользовательский бот-анкета на одинарную шкалу

@four_knightess_survey_bot
https://t.me/four_knightess_survey_bot
6707721562:AAG63YPyOrcw_LfcIh3x_NuInlSl1hY5cac
"""

from random import shuffle

from telebot import TeleBot
from telebot import types
from telebot.types import Message

from questions import questions

questions_max_score = {}
for test in questions:
    questions_max_score[test] = 0
    for t in questions[test]:
        questions_max_score[test] += max(list(t["a"].values()))
print(questions_max_score)

TOKEN = "6707721562:AAG63YPyOrcw_LfcIh3x_NuInlSl1hY5cac"
bot = TeleBot(TOKEN)

users = {}


def check_user(uid):
    if uid not in users:
        users[uid] = {
            'current_knightess': 'geography',
            'geography': {'score': 0, 'q_num': 0},
            'astronomy': {'score': 0, 'q_num': 0},
            'math': {'score': 0, 'q_num': 0},
            'literature': {'score': 0, 'q_num': 0},

        }
    print(users)


# Пустое меню, пригодится в конце анкеты.
hideKeyboard = types.ReplyKeyboardRemove()

# Стартовое меню, пригодится в конце анкеты.
menu_main = {
    'geography': '🌎 География',
    'astronomy': '🔭 Астрономия',
    'math': '🔢 Математика',
    'literature': '📚 Литература',
}
menu_result = {
    'result': '🔮 результат'
}
menu_break = {
    'break': '❌ Прервать этот тест'
}

FourKnightessOnlyKeyboard = types.ReplyKeyboardMarkup(
    row_width=4,
    resize_keyboard=True
)
FourKnightessOnlyKeyboard.add(* menu_main.values())

ResultOnlyKeyboard = types.ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True
)
ResultOnlyKeyboard.add(* menu_result.values())

FourKnightessKeyboard = types.ReplyKeyboardMarkup(
    row_width=5,
    resize_keyboard=True
)
FourKnightessKeyboard.add(* menu_main.values())
FourKnightessKeyboard.add(* menu_result.values())


@bot.message_handler(commands=['start'])
def handle_start(m: Message):
    """Приветствие, выбор из 4 тестов"""
    m.text = "/start"
    print("handle_start" + m.text)
    uid = str(m.from_user.id)
    check_user(uid)
    bot.send_message(
        m.from_user.id,
        "<b>Гой еси, красный молодец али красна девица!\n"
        "Истинно говорю тебе: последние времена наступают!</b>\n\n"
        "Грядут четыре всадникессы Анкетного Апокалипсиса,\n"
        "🏇🏻🏇🏇🏇🏻\n"
        "и имена им суть География, Астрономия, Математика и Литература. "
        "От каждой из них тебе предстоит выдержать по 10 ударов.\n\n"
        "И назначено тебе будет в конце испытаний: <b>паки-паки иже "
        "херувимы</b> или <b>кричать <i>Свободная касса</i> до пенсии</b>.\n\n"
        "Подробнее - в справке /help",

        parse_mode="HTML",
        reply_markup=FourKnightessKeyboard
    )


@bot.message_handler(commands=['help'])
def handle_help(m: Message):
    """Чуть более подробная справка"""
    print("handle_help" + m.text)
    bot.send_message(
        m.from_user.id,
        "Пройди в любом порядке четыре теста, узнай свою судьбу.\n\n"
        "Если отвечал, как дитё неразумное, и устыдился результатов "
        "позорных, то жми /reload и выступи по-богатырски.\n\n"
        "Результаты твои живут тут: /result",

        parse_mode="HTML",
        reply_markup=FourKnightessKeyboard
    )


@bot.message_handler(commands=['reload'])
def handle_reload(m: Message):
    """Чуть более подробная справка"""
    print("handle_reload" + m.text)
    uid = str(m.from_user.id)
    check_user(uid)
    users[uid] = {
        'current_knightess': 'geography',
        'geography': {'score': 0, 'q_num': 0},
        'astronomy': {'score': 0, 'q_num': 0},
        'math': {'score': 0, 'q_num': 0},
        'literature': {'score': 0, 'q_num': 0},
    }
    bot.send_message(
        m.from_user.id,
        "Результаты всех тестов удалил. Пробуй с нуля!",

        parse_mode="HTML",
        reply_markup=FourKnightessKeyboard
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text in menu_result.values())
@bot.message_handler(commands=['result'])
def handle_result(m: Message):
    """Результаты тестов"""
    print("handle_result" + m.text)
    uid = str(m.from_user.id)
    check_user(uid)
    user = users[uid]
    mtext = f"<b>ШТОШ, вот результаты:</b>\n\n"
    all_done = True
    result = {}
    rw = {
        'geography': ['Антигеографический', 'негеографический',
                      'географический', 'географ', ],
        'astronomy': ['Антиастрономический', 'неастрономический',
                      'астрономический', 'астроном', ],
        'math': ['Антиматематический', 'нематематический',
                      'математический', 'математик', ],
        'literature': ['Антилитературный', 'нелитературный',
                      'литературный', 'литератор', ],
    }
    result_words = []
    for test in menu_main:
        if user[test]['q_num'] < len(questions[test]):
            all_done = False
            break

    # all_done = True
    if not all_done:
        for test in menu_main:
            if user[test]['q_num'] < len(questions[test]):
                mtext += f"{menu_main[test]}: не завершён /{test}\n\n"
                all_done = False
            else:
                mtext += f"{menu_main[test]}: {user[test]['score']}\n\n"
        mres = "\nПОЛНЫЙ результат <b>после выполнения всех четырёх тестов</b>!"
    else:
        for test in menu_main:
            result[test] = (
                int(100 * user[test]['score'] / questions_max_score[test]))
            user[test]['score_int'] = result[test]
            mtext += (f"{menu_main[test]}: <b>{user[test]['score']} из "
                      f"{questions_max_score[test]}</b> "
                      f"({result[test]}%)\n\n")
        for i in range(4):
            for test in menu_main:
                if user[test]['score_int'] == min(result.values()):
                    result_words.append(rw[test][i])
                    result[test] = 102
                    user[test]['score_int'] = 102
                    break

        mres = (f"Поздравляю! По итогам тестирования ты —\n\n"
                f"<b>{' '.join(result_words).upper()}</b>!\n")

    bot.send_message(
        m.from_user.id,
        mtext + mres + "\nХочешь пройти всё заново? Жми /reload",

        parse_mode="HTML",
        reply_markup=FourKnightessKeyboard
    )


@bot.message_handler(
    content_types=["text"],
    func=lambda m: m.text in menu_main.values())
@bot.message_handler(commands=list(menu_main.keys()))
def handle_anketa(m: Message):
    """Запускаем выбранную анкету"""
    print("handle_anketa" + m.text)
    if (m.text not in menu_main.values()
            and m.text[1:] not in list(menu_main.keys())):
        bot.register_next_step_handler(m, handle_anketa)
        bot.send_message(
            m.from_user.id,
            f"Выберите тест!",

            parse_mode="HTML",
            reply_markup= FourKnightessOnlyKeyboard
        )
        return

    uid = str(m.from_user.id)
    check_user(uid)
    knightess = [k for k, v in menu_main.items() if v == m.text]
    if not knightess:
        knightess = m.text.replace("/", "")
    else:
        knightess = knightess[0]
    # print(knightess)
    users[uid]["current_knightess"] = knightess
    bot.send_message(
        m.chat.id,
        f"<b>{menu_main[knightess].upper()}</b>",

        parse_mode="HTML",
        reply_markup=hideKeyboard
    )
    anketa(m)


def anketa(m):
    """uid уже должен быть в users, но подстрахуемся"""
    print("anketa" + m.text)
    uid = str(m.from_user.id)
    check_user(uid)
    # print(uid)
    user = users[uid]
    knightess = user['current_knightess']

    if m.text == list(menu_break.values())[0]:
        user[knightess]["q_num"] -= 1
        bot.register_next_step_handler(m, handle_result)
        bot.send_message(
            m.from_user.id,
            f"Тестирование прервано. Можете вернуться позже.",

            parse_mode="HTML",
            reply_markup= ResultOnlyKeyboard
        )
        return

    q = user[knightess]["q_num"]
    quest = questions[knightess]
    # Если сейчас не первый вопрос, значит уже пришёл ответ на предыдущий
    if 0 < q <= len(quest):
        try:
            user[knightess]["score"] += quest[q - 1]["a"][m.text]
        except KeyError:
            user[knightess]["score"] -= quest[q - 1]["penalty"]

    # Вопросы закончились
    if q >= len(quest):
        anketa_finish(m)
        return

    # вопросы анкеты в одной функции, пока не закончатся
    bot.register_next_step_handler(m, anketa)

    markup_answers = types.ReplyKeyboardMarkup(
        row_width=len(quest[q]["a"]),
        resize_keyboard=True
    )
    a = list(map(str, quest[q]["a"].keys()))
    shuffle(a)
    markup_answers.add(* a)
    markup_answers.add(* menu_break.values())

    bot.send_message(
        m.from_user.id,
        f"Вопрос №{q + 1}:\n"
        f"{quest[q]['q']}",

        parse_mode="HTML",
        reply_markup=markup_answers
    )
    user[knightess]["q_num"] += 1


def anketa_finish(m):
    print("anketa_finish" + m.text)
    uid = str(m.from_user.id)
    check_user(uid)
    # print(uid)
    user = users[uid]
    knightess = user['current_knightess']
    bot.send_message(
        m.from_user.id,
        f"🏆 Неплохо, неплохо!\n"
        f"Счёт в этом тесте: <b>{user[knightess]['score']}</b>\n\n"
        f"Насколько неплохо - узнаешь после прохождения всех тестов.",

        parse_mode="HTML",
        reply_markup=FourKnightessKeyboard
    )


@bot.message_handler(
    func=lambda message: True,
    content_types=[
        'audio', 'photo', 'voice', 'video', 'document',
        'text', 'location', 'contact', 'sticker'])
def handle_error(m: Message):
    """ Обработка всех остальных сообщений как ошибочных """
    bot.send_message(m.chat.id, 'Напиши /start для запуска анкеты')


print(TOKEN)
bot.polling()
