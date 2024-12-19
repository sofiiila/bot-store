"""
модуль контакты
"""
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from src.new_handlers.handler_types import CONTACTS
from src.init_app import db_client

from src.services.db_client_types import CategoriesEnum


logger = logging.getLogger(__name__)


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.
    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.
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
    context.user_data['contacts'] = query.data
    logger.info("Пользователь %s добавил контакты: %s", user.first_name, query.data)

    # TODO Здесь нужно получить по id и обновить через метод fill в Invoice + метод in_queue
    db_client.update(filter_query={"user_id": user.id,
                                   "id": context.user_data['id'],
                                   "category": CategoriesEnum.QUEUE},
                     value={"contacts": query.data})

    await query.edit_message_text(
            text="Спасибо, что оставили ваши контакты! ТЗ принято в обработку."
        )

    return CONTACTS
