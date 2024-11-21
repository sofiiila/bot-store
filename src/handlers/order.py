from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import TZ
from src.logger import logger


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s chose to place an order.", user.first_name)
    await update.message.reply_text(
        "Пожалуйста, укажите техническое задание (ТЗ).",
        reply_markup=ReplyKeyboardRemove(),
    )
    return TZ
