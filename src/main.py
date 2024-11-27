import sys
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# Добавляем путь к src в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.handlers import start, menu, question, order, tz, files, skip_files, deadline, contacts, cancel, skip_tz, \
    skip_contacts, skip_question, skip_deadline, ask_more, continue_or_new
from src.handlers.handler_types import WRITE, QUESTION, ORDER, TZ, FILES, DEADLINE, CONTACTS, ASK_MORE, CONTINUE_OR_NEW
from src.settings import settings
from src.logger import init_logger


def main() -> None:
    load_dotenv()
    init_logger()

    application = Application.builder().token(settings.token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
            TZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, tz), CommandHandler("skip", skip_tz)],
            FILES: [MessageHandler(filters.Document.ALL, files), CommandHandler("skip", skip_files)],
            DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline), CommandHandler("skip", skip_deadline)],
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question), CommandHandler("skip", skip_question)],
            CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacts), CommandHandler("skip", skip_contacts)],
            ASK_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_more)],
            CONTINUE_OR_NEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, continue_or_new)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
