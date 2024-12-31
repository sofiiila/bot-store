"""
module order
"""
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.new_handlers.deadline import deadline
from src.init_app import controller
from src.new_handlers import ORDER, START, DEADLINE

logger = logging.getLogger(__name__)


async def handle_user_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    logger.critical(update.message.text)
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"tz": update.message.text})
    return await deadline(update, context)


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для заказа.
    """
    query = update.callback_query
    # Уведомление Telegram о том, что мы обработали нажатие кнопки.
    await query.answer()

    user = query.from_user
    logger.info("Пользователь %s выбрал заказать.", user.first_name)
    buttons = [
        [InlineKeyboardButton(text="В главное меню", callback_data=str(START))],
        [InlineKeyboardButton(text="Пропустить. Следующий вопрос.", callback_data=str(DEADLINE))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.message.reply_text("Укажите ваше ТЗ:", reply_markup=keyboard)
    await update.callback_query.answer()
    return ORDER
