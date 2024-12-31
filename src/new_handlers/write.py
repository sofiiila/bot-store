"""
module write.py
"""
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.start import start
from src.new_handlers.handler_types import WRITE, START

logger = logging.getLogger(__name__)


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    logger.critical(update.message.text)
    invoice = controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"question": update.message.text})
    invoice.push_in_queue()
    await update.message.reply_text("Ваше сообщение было отправлено. Мы скоро с вами свяжемся.")
    return await start(update, context)


async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения вопроса пользователя.
    Эта функция сохраняет вопрос пользователя и запрашивает контактные данные.
    """
    user = update.message.from_user if update.message else update.callback_query.from_user
    logger.info("Пользователь %s пишет нам.", user.first_name)
    buttons = [
        [InlineKeyboardButton(text="В главное меню", callback_data=str(START))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.message.reply_text("Введите ваше сообщение:", reply_markup=keyboard)
    await update.callback_query.answer()
    return WRITE
