"""
module stsrt
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.handler_types import ORDER, WRITE, START


logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отображает главное меню, независимо от того, идет ли вызов из команды или из кнопки.
    """
    buttons = [
        [InlineKeyboardButton(text="Заказать", callback_data=str(ORDER))],
        [InlineKeyboardButton(text="Написать нам", callback_data=str(WRITE))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if update.message:
        logger.critical(f"Вызвана команда /start. Вызвано сообщением с командой update.message={update.message}")
        user = update.message.from_user
        controller.update_document_for_user_id(user_id=user.id)
        await update.message.reply_text(
            "Главное меню.",
            reply_markup=keyboard,
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Главное меню.",
            reply_markup=keyboard
        )
        await update.callback_query.answer()

    return START
