"""
module order
"""
import logging

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import WRITE, QUESTION, TZ


logger = logging.getLogger(__name__)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для выбора пользователя.
        Эта функция обрабатывает выбор пользователя и переходит к соответствующему состоянию.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
         предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    choice = update.message.text

    if choice == "Написать нам":
        logger.info("Пользователь %s выбрал написать нам.", user.first_name)
        context.user_data['source'] = 'write'
        # pylint: disable=duplicate-code
        await update.message.reply_text(
            "Здесь вы можете задать любой вопрос или отправьте /skip, чтобы пропустить этот шаг.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return QUESTION
    if choice == "Заказать":
        logger.info("Пользователь %s выбрал заказать.", user.first_name)
        context.user_data['source'] = 'order'

        await update.message.reply_text(
            "Пожалуйста, укажите техническое задание (ТЗ) или отправьте /skip, "
            "чтобы пропустить этот шаг.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return TZ

    await update.message.reply_text(
        "Пожалуйста, выберите один из предложенных вариантов.",
        reply_markup=ReplyKeyboardMarkup(
            [["Написать нам", "Заказать"]], one_time_keyboard=True
        ),
    )
    return WRITE
