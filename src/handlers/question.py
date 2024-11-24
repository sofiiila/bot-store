from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import CONTACTS
from src.logger import logger


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения вопроса пользователя.
    Эта функция сохраняет вопрос пользователя и запрашивает контактные данные.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    context.user_data['question'] = update.message.text
    logger.info("Пользователь %s пишет нам: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS
