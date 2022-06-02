from functools import partial
import logging
import os
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater

from .answer_generator import AnswerGenerator

STRINGS = {"hello": "Давай поболтаем."}
REMEMBER_HISTORY = 3


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=STRINGS["hello"])


def answer(gen: AnswerGenerator, update: Update, context: CallbackContext):
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

    gen = AnswerGenerator()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, partial(answer, gen)))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://{HOSTNAME}/{TOKEN}")
    updater.idle()


if __name__ == "__main__":
    main()
