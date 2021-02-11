# Copyright (c) 2020 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Common globals and settings for the :mod:`gol` module."""
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SAVE_DIR = CURRENT_DIR / "data"
SAVE_DIR.mkdir(exist_ok=True)
SAVE_FILE = SAVE_DIR / "push_ups_save.json"
