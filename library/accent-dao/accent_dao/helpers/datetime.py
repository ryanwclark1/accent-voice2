# Copyright 2025 Accent Communications
from datetime import UTC, datetime


def utcnow_with_tzinfo() -> datetime:
    """Return current UTC datetime with timezone info.

    Returns:
        datetime: The current UTC datetime with timezone information.

    """
    return datetime.now(UTC)
