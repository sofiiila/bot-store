"""
module skip tz
"""
import logging

from telegram import Update, ReplyKeyboardRemove
from src.handlers.handler_types import FILES

logger = logging.getLogger(__name__)


async def skip_tz(update: Update) -> int:
    """
    Обработчик для пропуска шага ТЗ.
    Эта функция позволяет пользователю пропустить шаг приложения файлов
     и перейти к указанию срока выполнения.
    Args:
        update (Update): Объект, содержащий информацию о событии,
        которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста,
         предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользовптель %s пропустил добавление ТЗ.", user.first_name)
    await update.message.reply_text(
        "Приложите файлы, если необходимо, или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return FILES
