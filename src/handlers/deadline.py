"""
module deadline
"""
import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import CONTACTS
from src.init_app import db_client

from src.services.db_client_types import CategoriesEnum

logger = logging.getLogger(__name__)


async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения срока выполнения.
    Эта функция сохраняет срок выполнения и запрашивает контактные данные пользователя.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    if context.user_data is None:
        context.user_data = {}
    context.user_data['deadline'] = update.message.text
    logger.info("Пользователь %s добавил deadline: %s", user.first_name, update.message.text)

    # TODO Здесь нужно получить по id и обновить через метод fill в Invoice
    db_client.update(filter_query={"user_id": user.id,
                                   "id": context.user_data['id'],
                                   "category": CategoriesEnum.NEW},
                     value={"deadline": update.message.text})
    # pylint: disable=duplicate-code
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные или отправьте /skip,"
        " чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS
