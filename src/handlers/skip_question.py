from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.handlers.handler_types import CONTACTS
from src.logger import logger


async def skip_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для пропуска шага приложения файлов.
    Эта функция позволяет пользователю пропустить шаг приложения файлов и перейти к указанию срока выполнения.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользовптель %s пропустил добавление сообщения.", user.first_name)
    await update.message.reply_text(
        "Пожалуйста, оставьте свои контактные данные или отправьте /skip, чтобы пропустить этот шаг.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CONTACTS