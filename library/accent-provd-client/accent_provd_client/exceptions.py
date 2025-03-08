# Copyright 2023 Accent Communications

from requests import HTTPError


class ProvdError(HTTPError):
    def __init__(self, *args, **kwargs):
        response = kwargs.get('response', None)
        self.status_code = getattr(response, 'status_code', None)
        super().__init__(*args, **kwargs)


class ProvdServiceUnavailable(Exception):
    pass


class InvalidProvdError(Exception):
    pass
