"""
module skip files
"""
import logging

from telegram import Update, ReplyKeyboardRemove
from src.handlers.handler_types import DEADLINE

logger = logging.getLogger(__name__)


async def skip_files(update: Update) -> int:
    """
    Обработчик для пропуска шага приложения файлов.
    Эта функция позволяет пользователю пропустить шаг
    приложения файлов и перейти к указанию срока выполнения.
    Args:
        update (Update): Объект, содержащий информацию о событии,
         которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
        предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользовптель %s пропустил добавление файлов.", user.first_name)
    await update.message.reply_text(
        "Укажите срок выполнения или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEADLINE
