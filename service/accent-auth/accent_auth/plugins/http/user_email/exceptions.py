# Copyright 2023 Accent Communications

from accent_auth.exceptions import APIException


class EmailAlreadyConfirmedException(APIException):
    def __init__(self, email_uuid):
        msg = f'This email already confirmed: "{email_uuid}"'
        details = {'uuid': str(email_uuid)}
        super().__init__(409, msg, 'conflict', details, 'emails')
