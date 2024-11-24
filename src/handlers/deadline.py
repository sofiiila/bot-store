from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import CONTACTS
from src.logger import logger


async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения срока выполнения.
    Эта функция сохраняет срок выполнения и запрашивает контактные данные пользователя.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    context.user_data['deadline'] = update.message.text
    logger.info("Пользователь %s добавил deadline: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS
