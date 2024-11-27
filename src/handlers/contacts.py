from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from src.logger import logger
from src.services.db_client import update_user_data


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для получения контактных данных пользователя.
    Эта функция сохраняет контактные данные пользователя и записывает данные в базу данных.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    context.user_data['contacts'] = update.message.text
    logger.info("Пользователь %s добавил контакты: %s", user.first_name, update.message.text)

    update_user_data(user.id, "contacts", update.message.text)

    if context.user_data['source'] == 'write':
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты! Будем на связи!",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты! ТЗ принято в обработку.",
            reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END


