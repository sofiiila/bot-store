"""
module order
"""
import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.new_handlers.deadline import deadline
from src.init_app import controller
from src.new_handlers.handler_types import CANCEL_FILLING_BUTTON, DEADLINE, NEXT_STEP_BUTTON, \
    ORDER, START
from src.new_handlers.utills import basic_handler_for_step_in_question_list, save_media

logger = logging.getLogger(__name__)

STEP = "Указание ТЗ"
LOG_MESSAGE = "Пользователь %s указывает ТЗ"
MESSAGE = "Что требуется сделать(вы можете прикрепить файл):"


async def handle_user_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик сообщений, который может содержать текст, фото и документы.
    """
    user_id = update.message.from_user.id  # id пользователя из тг

    if update.message.caption or update.message.text:
        text = update.message.caption or update.message.text
        controller.update_document_for_user_id(user_id=user_id, update_fields={"tz": text})

    if update.message.photo:
        await save_media(update.message.photo[-1], user_id, "photo", ".jpg")
    if update.message.document:
        await save_media(update.message.document, user_id, "document",
                         update.message.document.file_name)
    if update.message.video:
        await save_media(update.message.video, user_id, "video", ".mp4")
    if update.message.audio or update.message.voice:
        audio = update.message.audio if update.message.audio else update.message.voice
        await save_media(audio, user_id, "audio", ".ogg")

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
