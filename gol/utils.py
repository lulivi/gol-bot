# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Utitilites for the push-ups counter."""
from datetime import datetime


def is_weekend() -> bool:
    """Checks if the current day is weekend.

    :returns: True when the current day is weekend.

    """
    return datetime.today().weekday() > 3
