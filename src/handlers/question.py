from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import CONTACTS
from src.logger import logger


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data['question'] = update.message.text
    logger.info("User %s asked a question: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS
