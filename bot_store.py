import logging
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start для Telegram-бота.

    Эта функция отправляет приветственное сообщение пользователю, который отправил команду /start.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.
    Returns:
        None
    """
    chat = update.effective_chat
    await context.bot.send_message(chat_id=chat.id, text='Привет, я bot_store!')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик для отображения меню с кнопками.

    Эта функция отправляет сообщение с клавиатурой ответа, содержащей кнопки "Написать нам" и "Заказать",
    и приветственное сообщение пользователю, который обратился к боту.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Написать нам', 'Заказать']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы обратились к нам, {name}!',
        reply_markup=button
    )


async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик для заказа.

    Эта функция отправляет сообщение пользователю с инструкцией указать техническое задание (ТЗ)
    и приложить файлы, если это необходимо. Также предоставляет кнопку для возврата к главному меню.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    back_button = ReplyKeyboardMarkup([['В главное меню']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Укажите ТЗ и приложите файлы, если необходимо.',
        reply_markup=back_button
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений.

    Эта функция проверяет текст сообщения от пользователя и выполняет соответствующие действия:
    - Если текст равен 'Заказать', вызывает функцию handle_order для обработки заказа.
    - Если текст равен 'Назад к главному меню', вызывает функцию menu для отображения главного меню.
    - В противном случае, отправляет сообщение 'Неизвестная команда.'.

    Args:
        update (Update): Объект, содержащий информацию о событии, которое вызвало эту функцию.
        context (ContextTypes.DEFAULT_TYPE): Объект контекста, предоставляющий доступ к боту и другим полезным данным.

    Returns:
        None
    """
    chat = update.effective_chat
    text = update.message.text
    if text == 'Заказать':
        await handle_order(update, context)
    elif text == 'Назад к главному меню':
        await menu(update, context)
    else:
        await context.bot.send_message(chat_id=chat.id, text='Я вас не понимаю')


def main() -> None:
    application = Application.builder().token(secret_token).build()

    application.add_handler(CommandHandler('start', menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
