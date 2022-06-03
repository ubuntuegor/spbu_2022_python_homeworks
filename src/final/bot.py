from functools import partial
import logging
import os
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater

from answer_generator import AnswerGenerator

STRINGS = {"hello": "Давай поболтаем."}
REMEMBER_HISTORY = 3


def start(update: Update, context: CallbackContext):
    if not update.effective_chat:
        raise RuntimeError("Wrong update passed to start handler")
    context.bot.send_message(chat_id=update.effective_chat.id, text=STRINGS["hello"])


def answer(gen: AnswerGenerator, update: Update, context: CallbackContext):
    if not update.message or not update.message.text or not update.effective_chat:
        raise RuntimeError("Wrong update passed to answer handler")
    if not isinstance(context.chat_data, dict):
        raise RuntimeError("chat_data unavailable")

    if "HISTORY" not in context.chat_data:
        context.chat_data["HISTORY"] = []
    history: list[str] = context.chat_data["HISTORY"]

    history.append(update.message.text)
    while len(history) > REMEMBER_HISTORY:
        history.pop(0)

    result = gen.generate(history)
    history.append(result)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def main():
    TOKEN = os.environ["TELEGRAM_TOKEN"]
    PORT = os.environ["PORT"]
    HOSTNAME = os.environ["WEBHOOK_HOSTNAME"]

    updater = Updater(TOKEN)
    dp = updater.dispatcher
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)

    gen = AnswerGenerator()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, partial(answer, gen)))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://{HOSTNAME}/{TOKEN}")
    logger.info("Bot successfully started")
    updater.idle()


if __name__ == "__main__":
    main()
