"""
module order
"""
import logging
import os

from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.new_handlers.deadline import deadline
from src.init_app import controller
from src.new_handlers.handler_types import CANCEL_FILLING_BUTTON, DEADLINE, NEXT_STEP_BUTTON, \
    ORDER, START
from src.new_handlers.utills import basic_handler_for_step_in_question_list

logger = logging.getLogger(__name__)

STEP = "Указание ТЗ"
LOG_MESSAGE = "Пользователь %s указывает ТЗ"
MESSAGE = "Что требуется сделать(вы можете прикрепить файл):"


async def handle_user_text_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик текстовых сообщений.
    """
    controller.update_document_for_user_id(user_id=update.message.from_user.id,
                                           update_fields={"tz": update.message.text})
    return await deadline(update, context)


async def handle_user_photo_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик фото сообщений.
    """
    photo_file = await update.message.photo[-1].get_file()
    file_path = os.path.join('downloads', f"user_photo_{update.message.from_user.id}.jpg")
    await photo_file.download_to_drive(file_path)
    logger.info(f"сохранено в: {file_path}")
    return await deadline(update, context)


async def handle_user_document_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик документов.
    """
    document = update.message.document
    file = await document.get_file()
    file_path = os.path.join('downloads', f"user_document_{update.message.from_user.id}.{document.file_name.split('.')[-1]}")
    await file.download_to_drive(file_path)
    logger.info(f"сохранено в: {file_path}")
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
