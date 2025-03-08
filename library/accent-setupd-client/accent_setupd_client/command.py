# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import (
    InvalidSetupdError,
    SetupdError,
    SetupdServiceUnavailable,
    SetupdSetupError,
)


class SetupdCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise SetupdServiceUnavailable(response)
        if response.status_code == 500:
            try:
                raise SetupdSetupError(response)
            except InvalidSetupdError:
                pass

        try:
            raise SetupdError(response)
        except InvalidSetupdError:
            RESTCommand.raise_from_response(response)
