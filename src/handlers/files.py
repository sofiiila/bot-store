"""
module files
"""
import logging
import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import DEADLINE
from src.init_app import db_client

from src.services.db_client_types import CategoriesEnum


logger = logging.getLogger(__name__)


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик документов.
    Обработчик для получения файлов.
    Скачивает документ, отправленный пользователем, и сохраняет его путь в user_data.
    Эта функция скачивает документ, отправленный пользователем, и сохраняет его путь в user_data.
    Переходит к шагу 'deadline' и запрашивает у пользователя срок выполнения.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """

    user = update.message.from_user
    file = await update.message.document.get_file()
    file_path = os.path.join('downloads', update.message.document.file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await file.download_to_drive(file_path)

    if context.user_data is None:
        context.user_data = {}

    context.user_data['files'] = file_path
    logger.info("Пользователь %s загрузил файл: %s", user.first_name, file_path)

    # TODO Здесь нужно получить по id и обновить через метод fill в Invoice
    db_client.update(filter_query={"user_id": user.id,
                                   "id": context.user_data['id'],
                                   "category": CategoriesEnum.NEW},
                     value={"files": update.message.text})

    await update.message.reply_text(
        "Укажите срок выполнения или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEADLINE
