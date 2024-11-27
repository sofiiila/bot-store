from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers.handler_types import WRITE, CONTINUE_OR_NEW
from src.services.db_client import update_user_data, get_user_state, set_user_state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды /start для Telegram-бота.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    user_state = get_user_state(user.id)

    if user_state:
        reply_keyboard = [["Продолжить заполнение", "Создать новую заявку"]]
        await update.message.reply_text(
            "Привет! Вы хотите продолжить заполнение предыдущей заявки или создать новую?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
            ),
        )
        return CONTINUE_OR_NEW
    else:
        update_user_data(user.id, "question", "No question")
        update_user_data(user.id, "tz", "No TZ")
        update_user_data(user.id, "files", "No files")
        update_user_data(user.id, "deadline", "No deadline")
        update_user_data(user.id, "contacts", "No contacts")
        set_user_state(user.id, None)

        reply_keyboard = [["Написать нам", "Заказать"]]
        await update.message.reply_text(
            "Привет, это bot_sore, здесь ты можешь оформить заказ или задать интересующий вопрос."
            "Отправь /cancel, если хочешь закончить разговор.\n\n",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
            ),
        )
        return WRITE