"""
Модуль ask_more обрабатывает запросы пользователей на получение дополнительной информации.

Этот модуль отвечает за обработку запросов типа 'ask more'
и предоставляет дополнительную информацию.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from src.handlers.handler_types import ASK_MORE, TZ, QUESTION


logger = logging.getLogger(__name__)


async def ask_more(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для оформления еще одного заказа.
        Эта функция обрабатывает выбор пользователя и переходит к соответствующему состоянию.
    Args:
        update (Update): Объект, содержащий информацию о событии,
         которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    choice = update.message.text

    if context.user_data is None:
        context.user_data = {}

    if choice == "Написать еще":
        logger.info("Пользователь %s выбрал написать еще.", user.first_name)
        context.user_data['source'] = 'write'
        # pylint: disable=duplicate-code
        await update.message.reply_text(
            "Здесь вы можете задать любой вопрос или отправьте /skip, чтобы пропустить этот шаг.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return QUESTION
    if choice == "Заказать еще":
        logger.info("Пользователь %s выбрал заказать еще.", user.first_name)
        context.user_data['source'] = 'order'
        await update.message.reply_text(
            "Пожалуйста, укажите техническое задание (ТЗ) или"
            " отправьте /skip, чтобы пропустить этот шаг.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return TZ
    # pylint: disable=duplicate-code
    reply_keyboard = [["Написать еще", "Заказать еще", "Назад"]]
    await update.message.reply_text(
        "Пожалуйста, выберите один из предложенных вариантов.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return ASK_MORE
