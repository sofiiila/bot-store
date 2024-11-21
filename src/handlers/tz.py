from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import FILES
from src.logger import logger


async def tz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data['tz'] = update.message.text
    logger.info("User %s provided TZ: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return FILES
