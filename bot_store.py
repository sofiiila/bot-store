import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, updater

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def say_hi(update, context):
    # Получаем информацию о чате и сохраняем в переменную chat
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,text='Привет, я bot_store!')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список,
    # даже если кнопка всего одна.
    button = ReplyKeyboardMarkup([['Написать нам', 'Заказать']],  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что вы обратились к нам, {}!'.format(name),
        # Добавим кнопку в содержимое отправляемого сообщения
        reply_markup=button
        )


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
