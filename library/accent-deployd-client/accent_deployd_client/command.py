# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import DeploydError, DeploydServiceUnavailable, InvalidDeploydError


class DeploydCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise DeploydServiceUnavailable(response)

        try:
            raise DeploydError(response)
        except InvalidDeploydError:
            RESTCommand.raise_from_response(response)
