# Copyright 2023 Accent Communications

from __future__ import annotations

import logging

from accent.rest_api_helpers import APIException

logger = logging.getLogger(__name__)


class TokenWithUserUUIDRequiredError(APIException):
    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            message='A valid token with a user UUID is required',
            error_id='token-with-user-uuid-required',
        )
