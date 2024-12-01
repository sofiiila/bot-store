import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для отмены диалога.
    Эта функция завершает диалог и отправляет сообщение пользователю.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользователь %s выбрал /cancel.", user.first_name)
    await update.message.reply_text(
        "До свидания! Надеюсь, в следующий раз вы решитесь оформить заказ.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
