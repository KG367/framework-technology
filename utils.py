"""Вспомогательные функции: работа с датами и ввод пользователя."""

from datetime import datetime
from typing import Optional

DATE_FORMAT = "%d.%m.%Y"
ISO_FORMAT = "%Y-%m-%d"


def parse_date(text: str) -> Optional[str]:
    """Преобразует дату из формата ДД.ММ.ГГГГ в ISO (YYYY-MM-DD)."""
    try:
        parsed = datetime.strptime(text.strip(), DATE_FORMAT)
    except (ValueError, AttributeError):
        return None
    return parsed.strftime(ISO_FORMAT)


def format_date(iso_date: str) -> str:
    """Преобразует ISO-дату в читаемый формат ДД.ММ.ГГГГ."""
    try:
        parsed = datetime.strptime(iso_date, ISO_FORMAT)
    except (ValueError, TypeError):
        return str(iso_date)
    return parsed.strftime(DATE_FORMAT)


def ask_int(prompt: str) -> Optional[int]:
    """Запрашивает у пользователя целое число.

    Возвращает None, если ввод пуст или не является числом.
    """
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None
