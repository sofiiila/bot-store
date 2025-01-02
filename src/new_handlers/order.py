"""
module order
"""
import logging

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.new_handlers.deadline import deadline
from src.init_app import controller
from src.new_handlers import ORDER, START, DEADLINE
from src.new_handlers.handler_types import CANCEL_FILLING_BUTTON, NEXT_STEP_BUTTON
from src.new_handlers.utills import basic_handler_for_step_in_question_list

logger = logging.getLogger(__name__)


STEP = "Указание ТЗ"
LOG_MESSAGE = "Пользователь %s указывает ТЗ"
MESSAGE = "Что требуется сделать:"


async def handle_user_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"tz": update.message.text})
    return await deadline(update, context)


async def order(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для заказа.
    """
    inline_buttons = [
        [InlineKeyboardButton(text=CANCEL_FILLING_BUTTON, callback_data=str(START))],
        [InlineKeyboardButton(text=NEXT_STEP_BUTTON, callback_data=str(DEADLINE))]
    ]
    await basic_handler_for_step_in_question_list(inline_buttons=inline_buttons, update=update,
                                                  log_message=LOG_MESSAGE, message=MESSAGE,
                                                  step=STEP)
    return ORDER
