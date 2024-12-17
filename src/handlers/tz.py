"""
MODULE TZ
"""
import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers import start
from src.handlers.handler_types import FILES
from src.init_app import db_client
from src.services.db_client_types import CategoriesEnum

logger = logging.getLogger(__name__)


async def tz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для ТЗ и пропуска шага ТЗ.
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

    if update.message.text == "/skip":
        logger.info("Пользователь %s пропустил добавление ТЗ.", user.first_name)
    elif update.message.text == "Назад":
        logger.info("54Пользователь %s отправил команду Назад.", user.first_name)
        return await start(update, context)
    else:
        context.user_data['tz'] = update.message.text
        logger.info("Пользователь %s добавил тз: %s", user.first_name, update.message.text)
        # TODO Здесь нужно получить по id и обновить через метод fill в Invoice
        db_client.update(filter_query={
            "user_id": user.id,
            # "id": str(context.user_data['id'])
            "category": CategoriesEnum.NEW
        },
                         value={"tz": update.message.text})

    reply_keyboard = [["Назад"]]
    await update.message.reply_text(
        "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return FILES
