from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from src.handlers.handler_types import CONTACTS
from src.logger import logger
from src.services.db_client import get_db_client


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data['contacts'] = update.message.text
    logger.info("User %s provided contacts: %s", user.first_name, update.message.text)

    client = get_db_client()
    db = client['mydatabase']
    collection = db['mycollection']

    document = {
        "user_id": user.id,
        "question": context.user_data.get('question', "No question"),
        "tz": context.user_data.get('tz', "No TZ"),
        "files": context.user_data.get('files', "No files"),
        "deadline": context.user_data.get('deadline', "No deadline"),
        "contacts": context.user_data['contacts']
    }

    collection.insert_one(document)
    if context.user_data['source'] == 'write':
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты!",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await update.message.reply_text(
            "Спасибо, что оставили ваши контакты! ТЗ принято в обработку.",
            reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END
