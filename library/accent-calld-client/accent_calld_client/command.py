# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import CalldError, InvalidCalldError


class CalldCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        try:
            raise CalldError(response)
        except InvalidCalldError:
            RESTCommand.raise_from_response(response)
