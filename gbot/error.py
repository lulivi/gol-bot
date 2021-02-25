# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Common errors in the :mod:`gbot` module."""


class BotError(Exception):
    """Base class for the bot errors."""

    pass


class TokenNotDefinedError(BotError):
    """The bot token is not defined."""

    pass
