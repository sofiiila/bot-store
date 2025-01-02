"""
module stsrt
"""
import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.handler_types import START

logger = logging.getLogger(__name__)


STEP = "Главное меню"
LOG_MESSAGE = "Пользователь %s зашел в главное меню"
MESSAGE = "Добро пожаловать в главное меню"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отображает главное меню, независимо от того, идет ли вызов из команды или из кнопки.
    """

    if update.message:
        query = update.message
        chat_id = update.message.chat.id

    else:
        query = update.callback_query
        await query.answer()
        chat_id = update.callback_query.message.chat.id
    controller.complete_old_or_create_new(query.from_user.id)
    user = query.from_user
    logger.info("Пользователь %s зашел в главное меню", user.username)
    await context.bot.send_message(
        text="Главное меню",
        chat_id=chat_id,
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(text='Написать нам'), KeyboardButton(text="Заказать")],
            ],
            resize_keyboard=True,
            one_time_keyboard=False)
    )
    return START
