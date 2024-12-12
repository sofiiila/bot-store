"""
module skip deafline
"""
import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from src.handlers.handler_types import CONTACTS

logger = logging.getLogger(__name__)


async def skip_deadline(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для пропуска шага дедлайн.
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
    logger.info("Пользовптель %s пропустил добавление дедлайна.",
                user.first_name)
    # pylint: disable=duplicate-code
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные или отправьте /skip,"
        " чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS
