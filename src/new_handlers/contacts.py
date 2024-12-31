"""
модуль контакты
"""
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.start import start
from src.new_handlers.handler_types import CONTACTS, START


logger = logging.getLogger(__name__)


async def handle_user_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    logger.critical(update.message.text)
    invoice = controller.update_document_for_user_id(
        user_id=update.message.from_user.id,
        update_fields={"contacts": update.message.text}
    )
    invoice.push_in_queue()
    await update.message.reply_text("Ваше сообщение было отправлено. Мы скоро с вами свяжемся.")
    return await start(update, context)


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
    logger.critical(update)
    query = update.message
    user = query.from_user
    logger.info("Пользователь %s добавил контакты: %s", user.first_name, query.text)
    buttons = [
        [InlineKeyboardButton(text="В главное меню", callback_data=str(START))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Укажите контакты для связи:", reply_markup=keyboard)
    return CONTACTS
