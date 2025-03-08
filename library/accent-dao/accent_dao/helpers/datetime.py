# Copyright 2023 Accent Communications
from datetime import datetime, timezone


def utcnow_with_tzinfo() -> datetime:
    return datetime.now(timezone.utc)
