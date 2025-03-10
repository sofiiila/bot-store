"""
модуль контакты
"""
import logging

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.init_app import controller

from src.new_handlers.start import start
from src.new_handlers.handler_types import CONTACTS, START, CANCEL_FILLING_BUTTON, \
    PREVIOUS_STEP_BUTTON, ORDER, NEXT_STEP_BUTTON
from src.new_handlers.utills import basic_handler_for_step_in_question_list

logger = logging.getLogger(__name__)


LOG_MESSAGE = "Пользователь %s указывает контакты"
MESSAGE = "Укажите дополнительные контакты для обратной связи:"
STEP = "Указание контактов"


async def handle_user_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, вводимых пользователем в состоянии WRITE,
    и отправка их по электронной почте.
    """
    if update.message:
        user_id = update.message.from_user.id
        obj_for_reply = update.message
        controller.update_document_for_user_id(
            user_id=user_id,
            update_fields={"contacts": update.message.text}
        )
    else:
        obj_for_reply = update.callback_query.message
    await obj_for_reply.reply_text("Ваша заяака отправлена. Мы скоро с вами свяжемся.")
    return await start(update, context)


async def contacts(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.
    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.
    """
    # Создаем клавиатуру для инлайн-кнопок
    inline_buttons = [
        [InlineKeyboardButton(text=CANCEL_FILLING_BUTTON, callback_data=str(START))],
        [InlineKeyboardButton(text=NEXT_STEP_BUTTON, callback_data="LAST_STATE"),
         InlineKeyboardButton(text=PREVIOUS_STEP_BUTTON, callback_data=str(ORDER))]
    ]

    await basic_handler_for_step_in_question_list(inline_buttons=inline_buttons, update=update,
                                                  log_message=LOG_MESSAGE, message=MESSAGE,
                                                  step=STEP)
    return CONTACTS
