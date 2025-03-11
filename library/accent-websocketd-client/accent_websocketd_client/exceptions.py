# Copyright 2025 Accent Communications



class WebsocketdClientException(Exception):
    """Base exception for websocketd client."""

    def __init__(
        self, message: str = "An error occurred with the websocketd client."
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message.

        """
        self.message = message
        super().__init__(self.message)


class AlreadyConnectedException(WebsocketdClientException):
    """Exception raised when attempting to modify connection settings while connected."""

    def __init__(
        self, message: str = "Cannot modify connection settings while connected."
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message.

        """
        super().__init__(message)


class NotRunningException(WebsocketdClientException):
    """Exception raised when attempting to use client before it's running."""

    def __init__(self, message: str = "Websocketd client is not running.") -> None:
        """Initialize the exception.

        Args:
            message: Error message.

        """
        super().__init__(message)


class ConnectionFailedException(WebsocketdClientException):
    """Exception raised when connection to websocketd server fails."""

    def __init__(
        self,
        message: str = "Failed to connect to websocketd server.",
        cause: Exception | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message.
            cause: The underlying exception that caused this error.

        """
        self.cause = cause
        super().__init__(message)
