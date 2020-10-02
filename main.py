import telebot
import db
import nlp

from telebot import types
from config import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = get_keyboard_choice()
    bot.send_message(message.chat.id,
                     'Приветствую мой дорогой друг {0.first_name}!\nЧем я могу быть полезен?'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    try:
        if message.chat.type == 'private':
            if message.text == 'Задать вопрос.':
                bot.send_message(message.chat.id, 'Просто введи свой вопрос в поле сообщений и отправь его мне.')

            elif message.text == 'Записаться к врачу.':
                db_records = ['20/06/2020', '25/06/2020', '01/07/2020']
                markup = get_inline_choice(db_records)

                bot.send_message(message.chat.id, 'Выберети подходящую запись.', reply_markup=markup)

            elif message.text == 'Убрать запись к врачу.':
                db.delete_client(telegram_user_id=message.chat.id)

                bot.send_message(message.chat.id, 'Ваша запись была успешна удалена.')

            else:
                """Answer the user message."""
                # getting an answer
                answer = nlp.classify_question(message.text)
                # sending message
                bot.send_message(message.chat.id, answer)

    except Exception as e:
        print(repr(e))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            # adding data in db
            db.add_client(
                telegram_user_id=call.message.chat.id,
                username=str(call.message.chat.first_name) + ' ' + str(call.message.chat.last_name),
                appointment_date=str(call.data)
            )

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Успех.\n' + str(call.data), reply_markup=None)
    except Exception as e:
        print(repr(e))


def get_keyboard_choice():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_question = types.KeyboardButton('Задать вопрос.')
    item_record_add = types.KeyboardButton('Записаться к врачу.')
    item_record_remove = types.KeyboardButton('Убрать запись к врачу.')

    markup.add(item_question)
    markup.add(item_record_add, item_record_remove)

    return markup


def get_inline_choice(db_records):
    markup = types.InlineKeyboardMarkup(row_width=len(db_records))

    for record in db_records:
        keyboard = types.InlineKeyboardButton(record, callback_data=record)
        markup.add(keyboard)

    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True)
