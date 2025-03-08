# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class DatabaseServiceUnavailable(Exception):
    def __init__(self):
        super().__init__('Postgresql is unavailable')


class TokenWithUserUUIDRequiredError(APIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            message='A valid token with a user UUID is required',
            error_id='token-with-user-uuid-required',
        )


class InvalidCallLogException(ValueError):
    pass


class ExportNotFoundException(APIException):
    def __init__(self, export_uuid):
        super().__init__(
            status_code=404,
            message='No export found matching this UUID',
            error_id='export-not-found-with-given-uuid',
            details={'export_uuid': str(export_uuid)},
        )


class CELInterpretationError(Exception):
    def __init__(self, event_name: str, raw_data=None):
        super().__init__(
            f'Failed to interpret event {event_name}.'
            + ('' if not raw_data else f' payload: {repr(raw_data)}')
        )
        self.event_name = event_name
        self.raw_data = raw_data
