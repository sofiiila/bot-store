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


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, который может содержать текст, фото и документы.
    """
    user_id = update.message.from_user.id

    if update.message.text:
        invoice = controller.update_document_for_user_id(user_id=user_id, update_fields={"tz": update.message.text})

    if update.message.photo:
        invoice = controller.update_document_for_user_id(user_id=user_id, update_fields={"tz": update.message.text})
        photo_file = await update.message.photo[-1].get_file()
        file_path = os.path.join(invoice.files_path, f"photo_{photo_file.file_id}.jpg")
        await photo_file.download_to_drive(file_path)
        logger.info(f"Фото сохранено в: {file_path}")

    if update.message.document:
        invoice = controller.update_document_for_user_id(user_id=user_id, update_fields={"tz": update.message.text})
        document = update.message.document
        file = await document.get_file()
        file_path = os.path.join(invoice.files_path, document.file_name)
        await file.download_to_drive(file_path)
        logger.info(f"Документ сохранен в: {file_path}")

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
