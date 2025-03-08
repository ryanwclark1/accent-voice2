# Copyright 2023 Accent Communications

from accent_auth.exceptions import _BaseParamException


class PasswordResetException(_BaseParamException):
    resource = 'reset'

    def __init__(self, message, details=None):
        super().__init__(message)

    @classmethod
    def from_errors(cls, errors):
        if list(errors.keys()) == ['_schema']:
            return cls(errors['_schema'])
        else:
            return super().from_errors(errors)
