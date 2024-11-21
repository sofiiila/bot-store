from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers.handler_types import WRITE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Написать нам", "Заказать"]]
    await update.message.reply_text(
        "Привет, это bot_sore, здесь ты можешь оформить заказ или задать интересующий вопрос."
        "Отправь /cancel, если хочешь закончить разговор.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
        ),
    )
    return WRITE