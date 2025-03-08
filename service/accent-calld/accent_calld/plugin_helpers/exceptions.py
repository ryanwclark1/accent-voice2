# Copyright 2023 Accent Communications

from accent_calld.exceptions import APIException


class BridgeNotFound(Exception):
    pass


class CalldUninitializedError(APIException):
    def __init__(self):
        super().__init__(
            status_code=503,
            message='accent-calld is not ready to handle this request',
            error_id='accent-calld-uninitialized',
        )


class TooManyChannels(Exception):
    def __init__(self, channels):
        self.channels = channels


class NotEnoughChannels(Exception):
    pass


class NoSuchConferenceID(Exception):
    def __init__(self, conference_id):
        self.conference_id = conference_id
        super().__init__(f'No such conference ID "{conference_id}"')


class NoSuchMeeting(Exception):
    def __init__(self, meeting_uuid):
        self.meeting_uuid = meeting_uuid
        super().__init__(f'No such meeting: UUID "{meeting_uuid}"')


class UserMissingMainLine(APIException):
    def __init__(self, user_uuid):
        super().__init__(
            status_code=400,
            message='User has no main line',
            error_id='user-missing-main-line',
            details={'user_uuid': user_uuid},
        )


class UserPermissionDenied(APIException):
    def __init__(self, user_uuid, details):
        details = dict(details)
        details['user'] = user_uuid
        super().__init__(
            status_code=403,
            message='User does not have permission to handle objects of other users',
            error_id='user-permission-denied',
            details=details,
        )


class InvalidExtension(APIException):
    def __init__(self, context, exten):
        super().__init__(
            status_code=400,
            message='Invalid extension',
            error_id='invalid-extension',
            details={
                'context': context,
                'exten': exten,
            },
        )


class InvalidUserUUID(APIException):
    def __init__(self, user_uuid):
        super().__init__(
            status_code=400,
            message='Invalid user: not found',
            error_id='invalid-user',
            details={'user_uuid': user_uuid},
        )


class InvalidUserLine(APIException):
    def __init__(self, user_id, line_id):
        super().__init__(
            status_code=400,
            message='User has no such line',
            error_id='invalid-user-line',
            details={
                'user_id': user_id,
                'line_id': line_id,
            },
        )


class NoSuchUserVoicemail(APIException):
    def __init__(self, user_uuid):
        super().__init__(
            status_code=404,
            message='No such user voicemail',
            error_id='no-such-user-voicemail',
            details={
                'user_uuid': user_uuid,
            },
        )


class NoSuchVoicemail(APIException):
    def __init__(self, voicemail_id):
        super().__init__(
            status_code=404,
            message='No such voicemail',
            error_id='no-such-voicemail',
            details={
                'voicemail_id': voicemail_id,
            },
        )


class AccentAmidError(APIException):
    def __init__(self, accent_amid_client, error, details=None):
        details = dict(details or {})
        details.update(
            {
                'accent_amid_config': {
                    'host': accent_amid_client.host,
                    'port': accent_amid_client.port,
                    'timeout': accent_amid_client.timeout,
                },
                'original_error': str(error),
            }
        )
        super().__init__(
            status_code=503,
            message='accent-amid request error',
            error_id='accent-amid-error',
            details=details,
        )


class AccentConfdUnreachable(APIException):
    def __init__(self, confd_client, error):
        super().__init__(
            status_code=503,
            message='accent-confd server unreachable',
            error_id='accent-confd-unreachable',
            details={
                'accent_confd_config': {
                    'host': confd_client.host,
                    'port': confd_client.port,
                    'timeout': confd_client.timeout,
                },
                'original_error': str(error),
            },
        )
