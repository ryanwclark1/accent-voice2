# Copyright 2023 Accent Communications

from accent_calld.exceptions import APIException


class NoSuchConfdUser(APIException):
    def __init__(self, user_uuid):
        super().__init__(
            status_code=400,
            message='No such confd user for the given authentication user',
            error_id='no-such-confd-user',
            details={'user_uuid': user_uuid},
        )


class NoSuchSwitchboard(APIException):
    def __init__(self, switchboard_uuid):
        super().__init__(
            status_code=404,
            message='No such switchboard',
            error_id='no-such-switchboard',
            details={'switchboard_uuid': switchboard_uuid},
        )


class NoSuchCall(APIException):
    def __init__(self, call_id):
        super().__init__(
            status_code=404,
            message='No such call',
            error_id='no-such-call',
            details={'call_id': call_id},
        )
