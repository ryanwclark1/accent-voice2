# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import (
    AmidError,
    AmidProtocolError,
    AmidServiceUnavailable,
    InvalidAmidError,
)


class AmidCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise AmidServiceUnavailable(response)

        try:
            raise AmidError(response)
        except InvalidAmidError:
            RESTCommand.raise_from_response(response)

    @staticmethod
    def raise_from_protocol(response):
        try:
            raise AmidProtocolError(response)
        except InvalidAmidError:
            RESTCommand.raise_from_response(response)
