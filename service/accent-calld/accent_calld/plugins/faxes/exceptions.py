# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class FaxFailure(APIException):
    def __init__(self, message):
        super().__init__(
            status_code=400,
            message=message,
            error_id='fax-failure',
        )
