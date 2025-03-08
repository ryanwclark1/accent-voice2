# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import HTTPCommand

from .exceptions import CallLogdError, CallLogdServiceUnavailable, InvalidCallLogdError


class CallLogdCommand(HTTPCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise CallLogdServiceUnavailable(response)

        try:
            raise CallLogdError(response)
        except InvalidCallLogdError:
            HTTPCommand.raise_from_response(response)
