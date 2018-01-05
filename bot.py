#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

import requests
FACT_URL = "https://catfact.ninja/fact"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def getApiKey():
    with open('TOKEN.txt') as f:
        return f.readline()

def messageFact(bot, update):
    text = update.message.text
    text = text.lower()
    if "cat" in text and "fact" in text:
        cat_fact = fetchFact()
        cat_fact and update.message.reply_text(cat_fact)

def inlineFact(bot, update):
    query = update.inline_query.query

    if not query:
        return

    cat_fact = fetchFact()

    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Cat Fact',
            input_message_content=InputTextMessageContent(cat_fact)
        )
    )

    bot.answer_inline_query(update.inline_query.id, results)



def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    key = getApiKey()
    updater = Updater(key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # message listener for catfacts
    dp.add_handler(MessageHandler(Filters.text, messageFact))

    # inline listener for catfacts
    dp.add_handler(InlineQueryHandler(inlineFact))
    dp.add_handler(MessageHandler(Filters.text, messageFact))

    # log all errors
    dp.add_error_handler(error)

    # start bot
    updater.start_polling()

    updater.idle()

def fetchFact():
    r = requests.get(FACT_URL)
    json = r.json()
    return json['fact']


if __name__ == '__main__':
    main()