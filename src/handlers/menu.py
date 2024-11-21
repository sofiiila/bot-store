from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import WRITE, QUESTION, TZ
from src.logger import logger


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    choice = update.message.text

    if choice == "Написать нам":
        logger.info("User %s chose to write a message.", user.first_name)
        context.user_data['source'] = 'write'
        await update.message.reply_text(
            "Здесь вы можете задать любой вопрос",
            reply_markup=ReplyKeyboardRemove(),
        )
        return QUESTION
    elif choice == "Заказать":
        logger.info("User %s chose to place an order.", user.first_name)
        context.user_data['source'] = 'order'
        await update.message.reply_text(
            "Пожалуйста, укажите техническое задание (ТЗ).",
            reply_markup=ReplyKeyboardRemove(),
        )
        return TZ
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=ReplyKeyboardMarkup(
                [["Написать нам", "Заказать"]], one_time_keyboard=True
            ),
        )
        return WRITE
