import logging

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, \
    CallbackQueryHandler, MessageHandler, filters, ContextTypes

from src.new_handlers.deadline import handle_user_deadline, deadline
from src.new_handlers.handler_types import START, ORDER, WRITE, CONTACTS, DEADLINE
from src.new_handlers.cancel import cancel
from src.new_handlers.start import start
from src.new_handlers.order import order, handle_user_tz
from src.new_handlers.write import write, handle_user_message
from src.new_handlers.contacts import contacts, handle_user_contacts


logger = logging.getLogger(__name__)


async def handle_global_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает сообщения от пользователя.

    Если текст сообщения равен "Написать нам", вызывает функцию write.
    Если текст сообщения равен "Заказать", вызывает функцию order.

    :param update: Объект обновления, содержащий информацию о сообщении.
    :param context: Контекст, содержащий информацию о текущем состоянии бота.
    :return: Результат выполнения функции write или order.
    """
    if update.message.text == "Написать нам":
        return await write(update, context)
    if update.message.text == "Заказать":
        return await order(update, context)

global_handler = MessageHandler(
    filters.TEXT & filters.Regex("^(Написать нам|Заказать)$"),
    handle_global_message
)
"""
Обработчик глобальных сообщений, фильтрующий текстовые сообщения,
соответствующие регулярному выражению "^(Написать нам|Заказать)$".
Вызывает функцию handle_global_message для обработки этих сообщений.
"""

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [
            global_handler,
            CallbackQueryHandler(order,
                                 pattern="^" + str(ORDER) + "$"),
            CallbackQueryHandler(write,
                                 pattern="^" + str(WRITE) + "$")
        ],
        ORDER: [
            global_handler,
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_tz),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
            CallbackQueryHandler(deadline, pattern="^" + str(DEADLINE) + "$")
        ],
        WRITE: [
            global_handler,
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
        ],
        CONTACTS: [
            global_handler,
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_contacts),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
            CallbackQueryHandler(deadline, pattern="^" + str(DEADLINE) + "$"),
            CallbackQueryHandler(handle_user_contacts, pattern="^" + "LAST_STATE" + "$")
        ],
        DEADLINE: [
            global_handler,
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_deadline),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
            CallbackQueryHandler(contacts, pattern="^" + str(CONTACTS) + "$"),
            CallbackQueryHandler(order, pattern="^" + str(ORDER) + "$")
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
"""
Основной обработчик диалога, управляющий состояниями и переходами между ними.
Использует ConversationHandler для управления состояниями и переходами.

:param entry_points: Точки входа в диалог.
:param states: Словарь состояний и соответствующих обработчиков.
:param fallbacks: Обработчики для завершения диалога.
"""
