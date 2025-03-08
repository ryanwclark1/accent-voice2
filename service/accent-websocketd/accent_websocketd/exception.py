# Copyright 2023 Accent Communications


class NoTokenError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class AuthenticationExpiredError(AuthenticationError):
    pass


class SessionProtocolError(Exception):
    pass


class BusConnectionError(Exception):
    pass


class BusConnectionLostError(BusConnectionError):
    pass


class UnsupportedVersionError(Exception):
    pass


class InvalidEvent(Exception):
    pass


class EventPermissionError(Exception):
    pass
