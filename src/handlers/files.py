import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import DEADLINE
from src.logger import logger


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    file = await update.message.document.get_file()
    file_path = os.path.join('downloads', update.message.document.file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await file.download_to_drive(file_path)
    context.user_data['files'] = file_path
    logger.info("User %s uploaded a file: %s", user.first_name, file_path)
    await update.message.reply_text(
        "Укажите срок выполнения.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEADLINE
