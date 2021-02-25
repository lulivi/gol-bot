# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Bot main executor."""
import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from gbot.commands import (
    command_config,
    command_error,
    command_help,
    command_push_ups,
    command_table,
    process_audio,
)
from gbot.error import TokenNotDefinedError
from gbot.settings import BOT_TOKEN, COUNTER
from gol.error import WrongCounterFileFormatError

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        raise TokenNotDefinedError("Could not find the token")

    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    # Commands
    dispatcher.add_handler(CommandHandler("help", command_help))
    dispatcher.add_handler(CommandHandler("config", command_config))
    dispatcher.add_handler(CommandHandler("flex", command_push_ups))
    dispatcher.add_handler(CommandHandler("flexiones", command_push_ups))
    dispatcher.add_handler(CommandHandler("error", command_error))
    dispatcher.add_handler(CommandHandler("table", command_table))

    # Filters
    dispatcher.add_handler(MessageHandler(Filters.voice, process_audio))

    try:
        COUNTER.load_count()
    except WrongCounterFileFormatError:
        logger.error("Couldn't load the file, configure the bot.")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
