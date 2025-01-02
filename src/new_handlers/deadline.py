"""
модуль контакты
"""
import logging

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.init_app import controller
from src.new_handlers.contacts import contacts
from src.new_handlers.handler_types import DEADLINE, START, CONTACTS, ORDER, \
    CANCEL_FILLING_BUTTON, PREVIOUS_STEP_BUTTON, NEXT_STEP_BUTTON
from src.new_handlers.utills import basic_handler_for_step_in_question_list

logger = logging.getLogger(__name__)


LOG_MESSAGE = "Пользователь %s указывает дедлайн"
MESSAGE = "Укажите сроки разработки:"
STEP = "Указание сроков"


async def handle_user_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"deadline": update.message.text})
    return await contacts(update, context)


async def deadline(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.
    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.
    """
    inline_buttons = [
        [InlineKeyboardButton(text=CANCEL_FILLING_BUTTON, callback_data=str(START))],
        [InlineKeyboardButton(text=NEXT_STEP_BUTTON, callback_data=str(CONTACTS)),
         InlineKeyboardButton(text=PREVIOUS_STEP_BUTTON, callback_data=str(ORDER))]

    ]
    await basic_handler_for_step_in_question_list(inline_buttons=inline_buttons, update=update,
                                                  log_message=LOG_MESSAGE, message=MESSAGE,
                                                  step=STEP)
    return DEADLINE
