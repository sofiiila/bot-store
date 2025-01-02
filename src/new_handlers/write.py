"""
module write.py
"""
import logging

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.start import start
from src.new_handlers.handler_types import WRITE, START, CANCEL_FILLING_BUTTON
from src.new_handlers.utills import basic_handler_for_step_in_question_list

logger = logging.getLogger(__name__)


STEP = "Написать нам."
LOG_MESSAGE = "Пользователь %s пишет нам"
MESSAGE = "Напишите нам по любым вопросам! Мы свяжемся с Вами как можно скорее."


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"question": update.message.text})
    await update.message.reply_text("Ваше сообщение было отправлено. Мы скоро с вами свяжемся.")
    return await start(update, context)


async def write(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения вопроса пользователя.
    Эта функция сохраняет вопрос пользователя и запрашивает контактные данные.
    """
    inline_buttons = [
        [InlineKeyboardButton(text=CANCEL_FILLING_BUTTON, callback_data=str(START))],
    ]
    await basic_handler_for_step_in_question_list(inline_buttons=inline_buttons, update=update,
                                                  log_message=LOG_MESSAGE, message=MESSAGE,
                                                  is_invoice=False)
    return WRITE
