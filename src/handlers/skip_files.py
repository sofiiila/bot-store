from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import DEADLINE
from src.logger import logger


async def skip_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s skipped the file upload step.", user.first_name)
    await update.message.reply_text(
        "Укажите срок выполнения.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEADLINE
