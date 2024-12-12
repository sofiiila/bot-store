"""
module stsrt
"""
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers.handler_types import WRITE
from src.init_app import db_client
from src.services.db_client_types import UserDocument


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды /start для Telegram-бота.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    # TODO через create Invoice
    document: UserDocument = db_client.create(user_id=user.id)
    if context.user_data is None:
        context.user_data = {}
    context.user_data['id'] = document.id
    reply_keyboard = [["Написать нам", "Заказать"]]
    await update.message.reply_text(
        "Привет, это bot_sore, здесь ты можешь оформить заказ или задать интересующий вопрос."
        "Отправь /cancel, если хочешь закончить разговор.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
        ),
    )
    return WRITE
