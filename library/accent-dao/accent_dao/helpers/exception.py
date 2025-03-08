# Copyright 2023 Accent Communications

class ServiceError(ValueError):
    template = "{prefix} - {message} {metadata}"
    prefix = "Error"

    def __init__(self, message=None, metadata=None):
        super().__init__(message)
        self.metadata = metadata


class InputError(ServiceError):
    prefix = "Input Error"


class ResourceError(ServiceError):
    prefix = "Resource Error"


class NotFoundError(ServiceError):
    prefix = "Resource Not Found"
