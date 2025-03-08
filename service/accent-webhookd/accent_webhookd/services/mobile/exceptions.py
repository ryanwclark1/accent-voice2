# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import Any

from accent_webhookd.services.helpers import HookExpectedError


class NotificationError(HookExpectedError):
    def __init__(self, details: dict[str, Any]) -> None:
        details.setdefault('error_id', 'notification-error')
        super().__init__(details)
