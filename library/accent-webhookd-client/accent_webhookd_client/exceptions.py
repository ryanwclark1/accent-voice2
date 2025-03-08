# Copyright 2023 Accent Communications

from __future__ import annotations

from requests import HTTPError, Response


class WebhookdError(HTTPError):
    def __init__(self, response: Response) -> None:
        try:
            body = response.json()
        except ValueError:
            raise InvalidWebhookdError()

        if not body:
            raise InvalidWebhookdError()

        self.status_code = response.status_code
        try:
            self.message = body['message']
            self.error_id = body['error_id']
            self.details = body['details']
            self.timestamp = body['timestamp']
        except KeyError:
            raise InvalidWebhookdError()

        exception_message = f'{self.message}: {self.details}'
        super().__init__(exception_message, response=response)


class WebhookdServiceUnavailable(WebhookdError):
    pass


class InvalidWebhookdError(Exception):
    pass
