# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class DuplicateUserException(APIException):
    def __init__(self):
        msg = 'Duplicate user detected'
        super().__init__(400, msg, 'duplicate-user', {}, 'rooms')
