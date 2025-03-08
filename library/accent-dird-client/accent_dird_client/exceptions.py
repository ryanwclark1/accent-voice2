# Copyright 2023 Accent Communications

from requests import HTTPError


class DirdError(HTTPError):
    def __init__(self, response):
        try:
            body = response.json()
        except ValueError:
            raise InvalidDirdError()

        if not body:
            raise InvalidDirdError()

        self.status_code = response.status_code
        try:
            self.message = body['message']
            self.error_id = body['error_id']
            self.details = body['details']
            self.timestamp = body['timestamp']

        except KeyError:
            raise InvalidDirdError()

        exception_message = f'{self.message}: {self.details}'
        super().__init__(exception_message, response=response)


class InvalidDirdError(Exception):
    pass


class DirdServiceUnavailable(DirdError):
    pass
