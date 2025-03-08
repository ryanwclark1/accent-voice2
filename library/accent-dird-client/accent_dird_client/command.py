# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import DirdError, DirdServiceUnavailable, InvalidDirdError


class DirdCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise DirdServiceUnavailable(response)

        try:
            raise DirdError(response)
        except InvalidDirdError:
            RESTCommand.raise_from_response(response)
