# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Common globals and settings for the :mod:`gbot` module."""
from pathlib import Path
from typing import Optional

from decouple import config

from gol.counter import PushUpsCounter

CURRENT_DIR = Path(__file__).resolve().parent
HELP_FILE: Path = CURRENT_DIR / "data" / "help.txt"
BOT_TOKEN: Optional[str] = config("GOL_BOT_TOKEN", cast=str, default=None)
COUNTER: PushUpsCounter = PushUpsCounter()
