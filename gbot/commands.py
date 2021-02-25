# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
#
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
"""Methods to allow commands and messages processing."""
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import PARSEMODE_MARKDOWN

from gbot.decorators import ensure_counter_initialization
from gbot.settings import COUNTER, HELP_FILE


def command_help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued.

    :param update: the update information.
    :param context: context for the current update.

    """
    update.message.reply_text(open(HELP_FILE, "r").read())


def command_config(update: Update, context: CallbackContext) -> None:
    """Configure the Push-Ups counter.

    :param update: the update information.
    :param context: context for the current update.

    """
    lines = update.message.text.splitlines()[1:]

    if len(lines) != 4:
        command_help(update, context)
        return

    COUNTER.config(*lines)


@ensure_counter_initialization(True)
def command_push_ups(update: Update, context: CallbackContext) -> None:
    """Add a new push-ups.

    :param update: the update information.
    :param context: context for the current update.

    """
    sender = str(update.message.from_user.id)
    receiber = (
        str(update.message.reply_to_message.from_user.id)
        if update.message.reply_to_message
        else COUNTER.opposite(sender)
    )
    COUNTER.add_pushups(
        receiber,
        sender,
    )


@ensure_counter_initialization(True)
def command_error(update: Update, context: CallbackContext) -> None:
    """Process an error push-up.

    :param update: the update information.
    :param context: context for the current update.

    """
    COUNTER.process_error(str(update.message.from_user.id))


@ensure_counter_initialization(True)
def command_table(update: Update, context: CallbackContext) -> None:
    """Send a table with the current push-up information.

    :param update: the update information.
    :param context: context for the current update.

    """
    update.message.reply_text(
        f"```{COUNTER.push_up_table()}```", parse_mode=PARSEMODE_MARKDOWN
    )


@ensure_counter_initialization()
def process_audio(update: Update, context: CallbackContext) -> None:
    """Process an audio message.

    :param update: the update information.
    :param context: context for the current update.

    """
    COUNTER.process_audio(str(update.message.from_user.id))
