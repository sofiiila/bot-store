import logging
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from secrets import db_user, db_password

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

WRITE, ORDER, TZ, FILES, DEADLINE, CONTACTS, QUESTION = range(7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды /start для Telegram-бота.

    Эта функция отправляет приветственное сообщение пользователю, который отправил команду /start.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        None
    """
    reply_keyboard = [["Написать нам", "Заказать"]]
    await update.message.reply_text(
        "Привет, это bot_sore, здесь ты можешь оформить заказ или задать интересующий вопрос."
        "Отправь /cancel, если хочешь закончить разговор.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return WRITE


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для выбора пользователя.

    Эта функция обрабатывает выбор пользователя и переходит к соответствующему состоянию.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    choice = update.message.text

    if choice == "Написать нам":
        logger.info("User %s chose to write a message.", user.first_name)
        await update.message.reply_text(
            "Здесь вы можете задать любой вопрос",
            reply_markup=ReplyKeyboardRemove(),
        )
        return QUESTION
    elif choice == "Заказать":
        logger.info("User %s chose to place an order.", user.first_name)
        await update.message.reply_text(
            "Пожалуйста, укажите техническое задание (ТЗ).",
            reply_markup=ReplyKeyboardRemove(),
        )
        return TZ
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=ReplyKeyboardMarkup(
                [["Написать нам", "Заказать"]], one_time_keyboard=True
            ),
        )
        return WRITE


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения вопроса пользователя.

    Эта функция сохраняет вопрос пользователя и запрашивает контактные данные.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    context.user_data['question'] = update.message.text
    logger.info("User %s asked a question: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONTACTS


async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    user = update.message.from_user
    logger.info("User %s chose to write a message.", user.first_name)
    await update.message.reply_text(
        "Здесь вы можете задать любой вопрос",
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONTACTS


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    user = update.message.from_user
    logger.info("User %s chose to place an order.", user.first_name)
    await update.message.reply_text(
        "Пожалуйста, укажите техническое задание (ТЗ).",
        reply_markup=ReplyKeyboardRemove(),
    )

    return TZ


async def tz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик текстовых сообщений.

    Проверяет текст сообщения от пользователя и выполняет соответствующие действия:
    - Если 'Заказать', вызывает функцию handle_order для обработки заказа.
    - Если 'В главное меню', вызывает функцию menu для отображения главного меню.
    - Если текст соответствует шагу 'tz', сохраняет ТЗ и переходит к шагу 'добавьте файлы'.
    - Если текст соответствует шагу 'deadline', сохраняет срок выполнения и запрашивает контактные данные пользователя.
    - В противном случае, отправляет сообщение 'Я вас не понимаю'.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    context.user_data['tz'] = update.message.text
    logger.info("User %s provided TZ: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return FILES


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения файлов.

    Эта функция скачивает документ, отправленный пользователем, и сохраняет его путь в user_data.
    Переходит к шагу 'deadline' и запрашивает у пользователя срок выполнения.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    file = await update.message.document.get_file()
    file_path = os.path.join('downloads', update.message.document.file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создаем директорию, если она не существует
    await file.download_to_drive(file_path)
    context.user_data['files'] = file_path
    logger.info("User %s uploaded a file: %s", user.first_name, file_path)
    await update.message.reply_text(
        "Укажите срок выполнения.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DEADLINE


async def skip_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для пропуска шага приложения файлов.

    Эта функция позволяет пользователю пропустить шаг приложения файлов и перейти к указанию срока выполнения.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    logger.info("User %s skipped the file upload step.", user.first_name)
    await update.message.reply_text(
        "Укажите срок выполнения.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DEADLINE


async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения срока выполнения.

    Эта функция сохраняет срок выполнения и запрашивает контактные данные пользователя.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    context.user_data['deadline'] = update.message.text
    logger.info("User %s provided deadline: %s", user.first_name, update.message.text)

    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONTACTS


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.

    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    context.user_data['contacts'] = update.message.text
    logger.info("User %s provided contacts: %s", user.first_name, update.message.text)

    # Сохранение данных в базу данных
    client = MongoClient(f'mongodb://{db_user}:{db_password}@localhost:27017/')
    db = client['mydatabase']
    collection = db['mycollection']

    document = {
        "user_id": user.id,
        "question": context.user_data.get('question', "No question"),
        "tz": context.user_data.get('tz', "No TZ"),
        "files": context.user_data.get('files', "No files"),
        "deadline": context.user_data.get('deadline', "No deadline"),
        "contacts": context.user_data['contacts']
    }

    result = collection.insert_one(document)
    await update.message.reply_text(
        "Спасибо, что оставили ваши контакты!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для отмены диалога.

    Эта функция завершает диалог и отправляет сообщение пользователю.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "До свидания! Надеюсь, в следующий раз вы решитесь оформить заказ.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """
    Главная функция для запуска .

    Настраивает и запускает бота, добавляя обработчики команд и сообщений.

    Returns:
        None
    """
    application = Application.builder().token(secret_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
            TZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, tz)],
            FILES: [MessageHandler(filters.Document.ALL, files), CommandHandler("skip", skip_files)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline)],
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question)],
            CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacts)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
