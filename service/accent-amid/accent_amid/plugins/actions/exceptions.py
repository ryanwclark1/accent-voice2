# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_amid.exceptions import APIException


class UnsupportedAction(APIException):
    def __init__(self, action: str) -> None:
        super().__init__(
            status_code=501,
            message='Action incompatible with accent-amid',
            error_id='incompatible-action',
            details={'action': action},
        )
