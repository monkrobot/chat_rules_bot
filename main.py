import logging
import os
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


token = os.environ['TOKEN']

functions = ['/version', 'import __hello__', 
            'import this', 'zen', '/about', 
            'from this import hi', 'from this import gist', 
            'from this import long_better', 'from this import correct', 
            'from this import offtopic', 'from this import politeness', 
            'from this import ask', 'from this import voice']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! This is autocomplite bot for spb_python_bot')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type @chat_rules_bot and start your query. This bot works only in \
chats with spb_python_bot')


def find_func(query_func):
    """Find autocomplite for inline query"""
    results = []
    
    for func in functions:
        if query_func in func:
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=func,
                    input_message_content=InputTextMessageContent(
                        func)),
            )
    return results


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = find_func(query)

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()