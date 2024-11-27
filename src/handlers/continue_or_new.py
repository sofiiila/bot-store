from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from src.handlers.handler_types import TZ, FILES, DEADLINE, CONTACTS, WRITE, CONTINUE_OR_NEW
from src.services.db_client import get_user_state, set_user_state, update_user_data


async def continue_or_new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    choice = update.message.text

    if choice == "Продолжить заполнение":
        user_state = get_user_state(user.id)
        if user_state == 'TZ':
            await update.message.reply_text(
                "Пожалуйста, укажите техническое задание (ТЗ) или отправьте /skip, чтобы пропустить этот шаг.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return TZ
        elif user_state == 'FILES':
            await update.message.reply_text(
                "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return FILES
        elif user_state == 'DEADLINE':
            await update.message.reply_text(
                "Укажите срок выполнения или отправьте /skip, чтобы пропустить этот шаг.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return DEADLINE
        elif user_state == 'CONTACTS':
            await update.message.reply_text(
                "Пожалуйста, оставьте свои контактные данные или отправьте /skip, чтобы пропустить этот шаг.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return CONTACTS
    elif choice == "Создать новую заявку":
        set_user_state(user.id, None)
        update_user_data(user.id, "question", "No question")
        update_user_data(user.id, "tz", "No TZ")
        update_user_data(user.id, "files", "No files")
        update_user_data(user.id, "deadline", "No deadline")
        update_user_data(user.id, "contacts", "No contacts")

        reply_keyboard = [["Написать нам", "Заказать"]]
        await update.message.reply_text(
            "Привет, это bot_sore, здесь ты можешь оформить заказ или задать интересующий вопрос."
            "Отправь /cancel, если хочешь закончить разговор.\n\n",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
            ),
        )
        return WRITE
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из предложенных вариантов.",
            reply_markup=ReplyKeyboardMarkup(
                [["Продолжить заполнение", "Создать новую заявку"]], one_time_keyboard=True
            ),
        )
        return CONTINUE_OR_NEW

