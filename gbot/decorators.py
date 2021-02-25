# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
#
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
"""Util decorators for the  :mod:`gbot` module."""
from typing import Callable

from telegram import Update
from telegram.ext import CallbackContext

from gbot.settings import COUNTER


def ensure_counter_initialization(
    warn: bool = False,
) -> Callable:
    """Ensure the counter is correctly configured.

    :param warn: bot function to run.

    """

    def inner(func: Callable) -> Callable:
        """Inner decorator function.

        :param func: bot function to run.

        """

        def wrapper(update: Update, context: CallbackContext) -> None:
            if COUNTER.is_configured():
                return func(update, context)

            if warn:
                update.message.reply_text(
                    "Please, configure the bot with /config first"
                )

        return wrapper

    return inner
