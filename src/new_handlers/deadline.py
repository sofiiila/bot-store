"""
модуль контакты
"""
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.contacts import contacts
from src.new_handlers.handler_types import DEADLINE, START


logger = logging.getLogger(__name__)


async def handle_user_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    logger.critical(update.message.text)
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"deadline": update.message.text})
    return await contacts(update, context)


async def deadline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.
    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.
    """
    logger.critical(update)
    buttons = [
        [InlineKeyboardButton(text="В главное меню", callback_data=str(START))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        query = update.message
        user = query.from_user
        logger.info("Пользователь %s указывает дедлайн", user.first_name)
        await update.message.reply_text("Укажите дедлайн:", reply_markup=keyboard)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        user = query.from_user
        logger.info("Пользователь %s указывает дедлайн", user.first_name)
        await update.callback_query.message.reply_text("Укажите дедлайн:", reply_markup=keyboard)
    return DEADLINE
