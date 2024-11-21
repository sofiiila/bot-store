from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from src.logger import logger


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "До свидания! Надеюсь, в следующий раз вы решитесь оформить заказ.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
