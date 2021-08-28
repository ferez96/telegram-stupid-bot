#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from datetime import datetime

from sqlalchemy import create_engine
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Chat
import models as m

# ACCESS TOKEN
token = os.getenv("TELEGRAM_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token=token)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat.id
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.chat.html
    chat = bot.get_chat(chat_id=chat_id)  # type: Chat # get chat latest data

    # Add chat whenever someone type /start
    model = m.db_session.query(m.Group).filter(m.Group.id == chat_id).first()
    if model:  # if the group is existed, just active it
        model.status = m.Group.Status.active
        chat.send_message("Group activation completed!")
    else:  # create new record
        m.db_session.add(m.Group(id=chat.id, name=chat.title, created_at=datetime.now()))
        chat.send_message("Group register completed!")
    update.message.reply_text('Done')


# stop support the group
def stop(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat.id
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.chat.html
    chat = bot.get_chat(chat_id=chat_id)  # type: Chat # get chat latest data

    # Add chat whenever someone type /start
    model = m.db_session.query(m.Group).filter(m.Group.id == chat_id).first()
    if model:  # if the group is existed, just active it
        model.status = m.Group.Status.inactive
        chat.send_message("Group deactivation completed!")
    else:
        chat.send_message("You have never registered!")
    update.message.reply_text('Done')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def setup_db():
    # SQLite
    engine = create_engine("sqlite:///db.sqlite")
    m.Session.configure(bind=engine)
    # create all database
    # m.Base.metadata.drop_all(bind=engine)
    m.Base.metadata.create_all(bind=engine)
    logger.info("init DB successfully")


def main():
    """Start the bot."""
    setup_db()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
