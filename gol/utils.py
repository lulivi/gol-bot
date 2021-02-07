from datetime import datetime


def is_weekend() -> bool:
    return datetime.today().weekday() > 3
