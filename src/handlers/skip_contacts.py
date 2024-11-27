from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from src.logger import logger


async def skip_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик для пропуска шага контактов.
    Эта функция позволяет пользователю пропустить шаг приложения файлов и перейти к указанию срока выполнения.
    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        int: Следующее состояние.
    """
    user = update.message.from_user
    logger.info("Пользовптель %s пропустил добавление контактов.", user.first_name)
    await update.message.reply_text(
        "Тут что-то типа ну ладно потом заполните",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END