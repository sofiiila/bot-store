"""
module order
"""
import logging

from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.handler_types import ORDER

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
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    logger.info("Пользователь %s выбрал заказать.", user.first_name)
    context.user_data['source'] = 'order'
    
    await query.edit_message_text(
        text="Пожалуйста, укажите техническое задание (ТЗ) или отправьте /skip,"
             " чтобы пропустить этот шаг. Отправьте /cancel, чтобы вернуться в главное меню."
    )
    return ORDER
