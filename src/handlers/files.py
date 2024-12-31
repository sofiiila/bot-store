"""
module files
"""
import logging
import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from src.handlers import start
from src.handlers.handler_types import DEADLINE
from src.init_app import db_client

from src.db_client.db_client_types import CategoriesEnum


logger = logging.getLogger(__name__)


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик документов.
    Обрабатывает загрузку файлов или пропуск этого шага.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    if update.message.text == "В главное меню":
        logger.info("Пользователь %s отправил команду Назад.", user.first_name)
        return await start(update, context)         # type: ignore

    if update.message.document:
        # Обработка загрузки файла
        file = await update.message.document.get_file()
        file_path = os.path.join('downloads', update.message.document.file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        await file.download_to_drive(file_path)

        if context.user_data is None:
            context.user_data = {}

        context.user_data['files'] = file_path
        logger.info("Пользователь %s загрузил файл: %s", user.first_name, file_path)

        # Обновление базы данных
        db_client.update(filter_query={"user_id": user.id,
                                       "id": context.user_data['id'],
                                       "category": CategoriesEnum.NEW},
                         value={"files": update.message.text})

    else:
        # Обработка пропуска шага
        logger.info("Пользователь %s пропустил добавление файлов.", user.first_name)

    await update.message.reply_text(
        "Укажите срок выполнения или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardMarkup(
            [["В главное меню"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return DEADLINE
