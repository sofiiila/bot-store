"""
module question
"""
import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers import start
from src.handlers.handler_types import CONTACTS
from src.init_app import db_client

from src.services.db_client_types import CategoriesEnum

logger = logging.getLogger(__name__)


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    user = update.message.from_user
    logger.info("контекст %s",
                context.user_data['id']) # type: ignore
    if context.user_data is None:
        context.user_data = {}

    if update.message.text == "В главное меню":
        logger.info("Пользователь %s отправил команду Назад.", user.first_name)
        return await start(update, context)         # type: ignore
    context.user_data['question'] = update.message.text
    logger.info("Пользователь %s пишет нам: %s", user.first_name, update.message.text)

    # TODO Здесь нужно получить по id и обновить через метод fill в Invoice
    db_client.update(
        filter_query={"user_id": user.id,
                      "id": context.user_data['id'],
                      "category": CategoriesEnum.NEW},
        value={"question": update.message.text})
    # pylint: disable=duplicate-code
    reply_keyboard = [["В главное меню"]]
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные или отправьте /skip,"
        " чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CONTACTS
