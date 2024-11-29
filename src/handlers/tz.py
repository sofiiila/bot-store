from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import FILES
from src.init_app import db_client
from src.logger import logger


async def tz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для ТЗ.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    context.user_data['tz'] = update.message.text
    logger.info("Пользователь %s добавил  тз: %s", user.first_name, update.message.text)

    db_client.update_user_data(user.id, "tz", update.message.text)

    await update.message.reply_text(
        "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return FILES
