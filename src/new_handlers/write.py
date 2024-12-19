"""
module write.py
"""
from gzip import WRITE
import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers import start
from src.new_handlers.handler_types import WRITE
from src.init_app import db_client

from src.services.db_client_types import CategoriesEnum

logger = logging.getLogger(__name__)


async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения вопроса пользователя.
    Эта функция сохраняет вопрос пользователя и запрашивает контактные данные.
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
    logger.info("Пользователь %s пишет нам.", user.first_name)
    
    context.user_data['write'] = query.data
    logger.info("Пользователь %s пишет нам: %s", user.first_name, query.data)

    # TODO Здесь нужно получить по id и обновить через метод fill в Invoice
    db_client.update(
        filter_query={"user_id": user.id,
                      "id": context.user_data['id'],
                      "category": CategoriesEnum.NEW},
        value={"question": query.data})
    # pylint: disable=duplicate-code
    await query.edit_message_text(
        text="Пожалуйста, напишите ваш вопрос или отправьте /skip, чтобы пропустить этот шаг."
    )
    return WRITE

