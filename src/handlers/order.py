"""
module order
"""
import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import TZ

logger = logging.getLogger(__name__)


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для заказа.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользователь %s выбрал заказать.", user.first_name)
    if context.user_data is None:
        context.user_data = {}
    context.user_data['source'] = 'order'
    await update.message.reply_text(
        "Пожалуйста, укажите техническое задание (ТЗ) или отправьте /skip,"
        " чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return TZ
