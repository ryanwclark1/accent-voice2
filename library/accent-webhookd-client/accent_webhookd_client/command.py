# Copyright 2023 Accent Communications

from __future__ import annotations

from requests import Response
from accent_lib_rest_client.command import RESTCommand

from .exceptions import InvalidWebhookdError, WebhookdError, WebhookdServiceUnavailable


class WebhookdCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response: Response) -> None:
        if response.status_code == 503:
            raise WebhookdServiceUnavailable(response)

        try:
            raise WebhookdError(response)
        except InvalidWebhookdError:
            RESTCommand.raise_from_response(response)
