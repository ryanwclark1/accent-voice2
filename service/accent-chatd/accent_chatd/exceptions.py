# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class UnknownUserException(APIException):
    def __init__(self, user_uuid):
        msg = f'No such user: "{user_uuid}"'
        details = {'uuid': str(user_uuid)}
        super().__init__(404, msg, 'unknown-user', details, 'users')


class UnknownTenantException(APIException):
    def __init__(self, tenant_uuid):
        msg = f'No such tenant: "{tenant_uuid}"'
        details = {'uuid': str(tenant_uuid)}
        super().__init__(404, msg, 'unknown-tenant', details, 'tenants')


class UnknownSessionException(APIException):
    def __init__(self, session_uuid):
        msg = f'No such session: "{session_uuid}"'
        details = {'uuid': str(session_uuid)}
        super().__init__(404, msg, 'unknown-session', details, 'sessions')


class UnknownRefreshTokenException(APIException):
    def __init__(self, client_id, user_uuid):
        msg = f'No such refresh_token (client_id): "{client_id}"'
        details = {'client_id': client_id, 'user_uuid': str(user_uuid)}
        super().__init__(404, msg, 'unknown-refresh_token', details, 'refresh_tokens')


class UnknownLineException(APIException):
    def __init__(self, line_id):
        msg = f'No such line: "{line_id}"'
        details = {'id': line_id}
        super().__init__(404, msg, 'unknown-line', details, 'lines')


class UnknownEndpointException(APIException):
    def __init__(self, endpoint_name):
        msg = f'No such endpoint: "{endpoint_name}"'
        details = {'name': endpoint_name}
        super().__init__(404, msg, 'unknown-endpoint', details, 'endpoints')


class UnknownRoomException(APIException):
    def __init__(self, room_uuid):
        msg = f'No such room: "{room_uuid}"'
        details = {'uuid': str(room_uuid)}
        super().__init__(404, msg, 'unknown-room', details, 'rooms')
