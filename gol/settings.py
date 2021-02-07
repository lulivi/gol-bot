from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SAVE_DIR = CURRENT_DIR / "data"
SAVE_DIR.mkdir(exist_ok=True)
SAVE_FILE = SAVE_DIR / "push_ups_save.json"
