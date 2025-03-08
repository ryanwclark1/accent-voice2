# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class GoogleTokenNotFoundException(APIException):
    code = 404

    def __init__(self, user_uuid):
        message = 'No google token found.'
        details = {'user_uuid': user_uuid}
        super().__init__(self.code, message, 'no-token-found', details)
