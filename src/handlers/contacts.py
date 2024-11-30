from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from src.handlers.handler_types import ASK_MORE
from src.init_app import db_client
from src.logger import logger
from src.services.db_client_types import CategoriesEnum


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

    db_client.update(filter_query={"user_id": user.id,
                                   "id": context.user_data['id'],
                                   "category": CategoriesEnum.new},
                     value={"contacts": update.message.text})

    if context.user_data['source'] == 'write':
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты! Будем на связи!",
            reply_markup=ReplyKeyboardMarkup(
                [["Написать еще", "Заказать еще"]], one_time_keyboard=True, resize_keyboard=True
            ),
        )
    else:
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты! ТЗ принято в обработку.",
            reply_markup=ReplyKeyboardMarkup(
                [["Написать еще", "Заказать еще"]], one_time_keyboard=True, resize_keyboard=True
            ),
        )

    return ASK_MORE


