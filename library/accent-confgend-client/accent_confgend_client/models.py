#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Data models for the Accent Configuration Generator client."""

from pydantic import BaseModel, Field


class ConfgendConfig(BaseModel):
    """Configuration for the Accent Confgend client.

    Attributes:
        host: Hostname or IP address of the confgend server.
        port: Port number of the confgend server.
        timeout: Timeout in seconds for network operations.
        use_https: Whether to use HTTPS for communication.

    """

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8669)
    timeout: float = Field(default=5.0)
    use_https: bool = Field(default=False)

    @property
    def base_url(self) -> str:
        """Get the base URL for the confgend server."""
        protocol = "https" if self.use_https else "http"
        return f"{protocol}://{self.host}:{self.port}"


class ConfgendResponse(BaseModel):
    """Response from the Accent Confgend server.

    Attributes:
        content: The content of the configuration file.
        cached: Whether the content was served from cache.
        filename: The name of the requested configuration file.

    """

    content: bytes
    cached: bool = Field(default=False)
    filename: str
