import logging
import os
import sqlite3

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Создание таблицы для хранения заказов
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    tz TEXT,
    files TEXT,
    deadline TEXT
)
''')
conn.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start для Telegram-бота.

    Эта функция отправляет приветственное сообщение пользователю, который отправил команду /start.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        None
    """
    chat = update.effective_chat
    await context.bot.send_message(chat_id=chat.id, text='Привет, я bot_store!')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик для отображения меню с кнопками.

    Эта функция отправляет сообщение с клавиатурой ответа, содержащей кнопки "Написать нам" и "Заказать",
    и приветственное сообщение пользователю, который обратился к боту.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Написать нам', 'Заказать']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы обратились к нам, {name}!',
        reply_markup=button
    )


async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик для заказа.

    Эта функция отправляет сообщение пользователю с инструкцией указать техническое задание (ТЗ)
    и приложить файлы, если это необходимо. Также предоставляет кнопку для возврата к главному меню.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    back_button = ReplyKeyboardMarkup([['В главное меню']], resize_keyboard=True)
    context.user_data['step'] = 'tz'
    await context.bot.send_message(
        chat_id=chat.id,
        text='Укажите ТЗ и приложите файлы, если необходимо.',
        reply_markup=back_button
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений.

    Проверяет текст сообщения от пользователя и выполняет соответствующие действия:
    - Если 'Заказать', вызывает функцию handle_order для обработки заказа.
    - Если 'В главное меню', вызывает функцию menu для отображения главного меню.
    - Если текст соответствует шагу 'tz', сохраняет ТЗ и переходит к шагу 'добавьте файлы'.
    - Если текст соответствует шагу 'deadline', сохраняет срок выполнения и записывает данные в базу данных.
    - В противном случае, отправляет сообщение 'Я вас не понимаю'.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    text = update.message.text
    if text == 'Заказать':
        await handle_order(update, context)
    elif text == 'В главное меню':
        await menu(update, context)
    elif context.user_data.get('step') == 'tz':
        context.user_data['tz'] = text
        context.user_data['step'] = 'files'
        await context.bot.send_message(chat_id=chat.id, text='Приложите файлы, если необходимо.')
    elif context.user_data.get('step') == 'deadline':
        context.user_data['deadline'] = text
        # Сохранение данных в базу данных
        cursor.execute('''
            INSERT INTO orders (user_id, tz, files, deadline)
            VALUES (?, ?, ?, ?)
            ''', (chat.id, context.user_data['tz'], context.user_data.get('files', ''), context.user_data['deadline']))
        conn.commit()
        await context.bot.send_message(chat_id=chat.id, text='Ваше ТЗ принято в обработку!')
        await menu(update, context)
    else:
        await context.bot.send_message(chat_id=chat.id, text='Я вас не понимаю')


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик документов.

    Скачивает документ, отправленный пользователем, и сохраняет его путь в user_data.
    Переходит к шагу 'deadline' и запрашивает у пользователя срок выполнения.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    if context.user_data.get('step') == 'files':
        file = await context.bot.get_file(update.message.document.file_id)
        file_path = os.path.join('downloads', update.message.document.file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создаем директорию, если она не существует
        await file.download_to_drive(file_path)
        context.user_data['files'] = file_path
        context.user_data['step'] = 'deadline'
        await context.bot.send_message(chat_id=chat.id, text='Укажите срок выполнения.')
    else:
        await context.bot.send_message(chat_id=chat.id, text='Я вас не понимаю')


def main() -> None:
    """
    Главная функция для запуска Telegram-бота.

    Настраивает и запускает бота, добавляя обработчики команд и сообщений.

    Returns:
        None
    """
    application = Application.builder().token(secret_token).build()

    application.add_handler(CommandHandler('start', menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    application.run_polling()


if __name__ == '__main__':
    main()
