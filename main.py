#!/usr/bin/env python
# pylint: disable=C0116,W0613
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
import pdb

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_config import TOKEN
import find_a_partner.interaction.messaging as messaging
from find_a_partner.persistence import db
from find_a_partner.persistence.entities import User, Message
from find_a_partner.persistence.models.user import NewUser, UserLevel

# error messages
ERR_MSG_NOT_TRUSTED = 'Sorry, du kannst gerade noch keine Suchanfragen stellen. Mache folgendes, um das zu ändern: ...'
ERR_MSG_PREFIX_WRONG_AMOUNT_PARAMETERS = 'Sorry, falsche Anzahl an Parametern'
ERR_MSG_EXAMPLE_ADD_MESSAGE_REQUEST_COMMAND = 'Beispiel /suche Ich suche jemanden um ...'

# Enable logging
from find_a_partner.user_management.permission import ensure_required_user_level, trust_user, is_trusted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    # send welcome message
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! Warte bis du vertrauenswürdig bist\. Gebe dann /suche Ich suche \.\.\. ein um eine Suchanfrage abzuschicken\.',
        reply_markup=ForceReply(selective=True),
    )

    # persist user in database
    new_user = NewUser(telegram_id=update.message.from_user.id,
                       username=update.message.from_user.username)
    User.upsert(new_user)


def trust(update: Update, context: CallbackContext) -> None:
    """
    set user as trusted
    - example: /trust user123 reason why I trust this user
    @param update:
    @param context:
    """

    # ensure user has required user level
    if not ensure_required_user_level(update, UserLevel.ADMIN):
        # user does not have required user level
        return

    # validate input
    if len(context.args) < 2:
        update.message.reply_text('invalid number of arguments (must be /trust username reason why to trust)')
        return
    target_username = context.args[0]
    reason = ' '.join(context.args[1:])
    if User.get_by_username(target_username) is None:
        update.message.reply_text('user missing')
        return

    # set user as trusted
    trust_user(target_username, reason)


def add_message_request(update: Update, context: CallbackContext) -> None:
    """
    request to post message to other users
    - example: /suche The message
    @param update:
    @param context:
    """

    # ensure user is allowed to post message requests
    user = User.get_by_telegram_id(update.message.from_user.id)
    if not is_trusted(user.id):
        update.message.reply_text(ERR_MSG_NOT_TRUSTED)
        # user is not allowed to post message requests
        return

    # validate input
    if len(context.args) < 1:
        update.message.reply_text(f'{ERR_MSG_PREFIX_WRONG_AMOUNT_PARAMETERS}. '
                                  f'{ERR_MSG_EXAMPLE_ADD_MESSAGE_REQUEST_COMMAND}')
        return

    # add message request
    # - forward message request to all admins
    messaging.add_message_request(user, update.message.text)


def confirm_message_request(update: Update, context: CallbackContext) -> None:
    """
    confirm request to post message to other users
    - example: /ok 123
    @param update:
    @param context:
    """

    # ensure user has required user level
    if not ensure_required_user_level(update, UserLevel.ADMIN):
        # user does not have required user level
        return

    # validate input
    if len(context.args) < 1:
        update.message.reply_text('message id missing')
        return
    if len(context.args) > 1:
        update.message.reply_text('invalid number of arguments (must be /ok MESSAGE_ID')
        return
    message_id = int(context.args[0])
    if Message.get_by_id_non_throw(message_id) is None:
        update.message.reply_text('message missing (or message id wrong)')
        return

    # confirm message request
    # - forward message to all trusted users
    messaging.confirm_message_request(message_id)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('/start - Füge dich hinzu\n'
                              '/suche Hallo ich suche - Mache eine Anfrage (muss zuerst akzeptiert werden)\n'
                              '\n'
                              'Nur Admins: \n'
                              '/trust <Benutzername> <Grund> - Setze ein Mitglied auf vertrauenswürdig\n'
                              '/ok <NachrichtenID> - Quittiere eine Anfrage.\n'
                              'Wird an alle vertrauenswürdigen Benutzer weitergeleitet')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""

    # initialize database
    db.initialize()

    # TODO: check factor out?
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # - common commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # - admin commands
    dispatcher.add_handler(CommandHandler("trust", trust))
    dispatcher.add_handler(CommandHandler("ok", confirm_message_request))
    # - user commands
    dispatcher.add_handler(CommandHandler("suche", add_message_request))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    # tear down application
    db.tear_down()


if __name__ == '__main__':
    main()