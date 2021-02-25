# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Common errors in the :mod:`gol` module."""


class CounterError(Exception):
    """Errors related witht he PushUpsCounter class."""

    pass


class WrongCounterFileFormatError(CounterError, IOError):
    """There was an error when parsing the counter file."""

    pass


class ParticipantNotFound(CounterError):
    """GOL participant was not found."""

    pass
