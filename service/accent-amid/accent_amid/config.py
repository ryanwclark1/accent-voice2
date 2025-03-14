# src/accent_amid/config.py
from __future__ import annotations

import logging
import uuid
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AMISettings(BaseSettings):
    """Settings for the AMI client.

    Attributes:
        HOST (str): The AMI server hostname or IP address.
        PORT (int): The AMI server port.
        USERNAME (str): The AMI username.
        PASSWORD (str): The AMI password.

    """

    HOST: str = Field(default="localhost", validation_alias="ami_host")
    PORT: int = Field(default=5038, validation_alias="ami_port")
    USERNAME: str = Field(default="accent_amid", validation_alias="ami_username")
    PASSWORD: str = Field(default="password123", validation_alias="ami_password")


class AJAMSettings(BaseSettings):
    """Settings for the AJAM client.

    Attributes:
        HOST (str): The AJAM server hostname or IP address.
        PORT (int): The AJAM server port.
        USERNAME (str): The AJAM username.
        PASSWORD (str): The AJAM password.
        HTTPS (bool): Whether to use HTTPS for AJAM connections.

    """

    HOST: str = Field(default="localhost", validation_alias="ajam_host")
    PORT: int = Field(default=5039, validation_alias="ajam_port")
    USERNAME: str = Field(default="accent_amid", validation_alias="ajam_username")
    PASSWORD: str = Field(default="password123", validation_alias="ajam_password")
    HTTPS: bool = Field(default=False, validation_alias="ajam_https")


class AuthSettings(BaseSettings):
    """Settings for the authentication client.

    Attributes:
        HOST (str): The authentication server hostname or IP address.
        PORT (int): The authentication server port.
        PREFIX (str | None): The URL prefix for the authentication server.
        HTTPS (bool): Whether to use HTTPS for authentication server connections.
        KEY_FILE (str): Path to the key file.  Defaults to a dummy value, as a real path isn't known.

    """

    HOST: str = Field(default="localhost", validation_alias="auth_host")
    PORT: int = Field(default=9497, validation_alias="auth_port")
    PREFIX: str | None = Field(default=None, validation_alias="auth_prefix")
    HTTPS: bool = Field(default=False, validation_alias="auth_https")
    KEY_FILE: str = Field(
        default="/var/lib/dummy-key-file.yml", validation_alias="auth_key_file"
    )  # Dummy value


class BusSettings(BaseSettings):
    """Settings for the message bus (RabbitMQ).

    Attributes:
        HOST (str): The message bus hostname or IP address.
        PORT (int): The message bus port.
        USERNAME (str): The message bus username.
        PASSWORD (str): The message bus password.
        VHOST (str): The virtual host for the message bus.
        EXCHANGE_NAME (str): The exchange name for the message bus.
        EXCHANGE_TYPE (Literal['headers']): The exchange type.
        STARTUP_CONNECTION_DELAY (int): How long to wait between connection attempts.

    """

    HOST: str = Field(default="localhost", validation_alias="bus_host")
    PORT: int = Field(default=5672, validation_alias="bus_port")
    USERNAME: str = Field(default="guest", validation_alias="bus_username")
    PASSWORD: str = Field(default="guest", validation_alias="bus_password")
    VHOST: str = Field(default="/", validation_alias="bus_vhost")
    EXCHANGE_NAME: str = Field(
        default="accent-headers", validation_alias="bus_exchange_name"
    )
    EXCHANGE_TYPE: Literal["headers"] = Field(
        default="headers", validation_alias="bus_exchange_type"
    )
    STARTUP_CONNECTION_DELAY: int = Field(
        default=1, validation_alias="bus_startup_connection_delay"
    )


class RestApiSettings(BaseSettings):
    """Settings for the REST API.

    Attributes:
        LISTEN (str): The address to listen on.
        PORT (int): The port to listen on.
        CERTIFICATE (str | None): The path to the SSL certificate file.
        PRIVATE_KEY (str | None): The path to the SSL private key file.
        CORS_ENABLED (bool): Whether to enable CORS.
        CORS_ALLOW_HEADERS (list[str]): The list of allowed headers for CORS.
        MAX_THREADS (int): The maximum number of threads for the server.

    """

    LISTEN: str = Field(default="127.0.0.1", validation_alias="rest_api_listen")
    PORT: int = Field(default=9491, validation_alias="rest_api_port")
    CERTIFICATE: str | None = Field(
        default=None, validation_alias="rest_api_certificate"
    )
    PRIVATE_KEY: str | None = Field(
        default=None, validation_alias="rest_api_private_key"
    )
    CORS_ENABLED: bool = Field(default=True, validation_alias="rest_api_cors_enabled")
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=["Content-Type", "X-Auth-Token"],
        validation_alias="rest_api_cors_allow_headers",
    )
    MAX_THREADS: int = Field(default=10, validation_alias="rest_api_max_threads")


class Settings(BaseSettings):
    """Top-level settings for the application.

    Attributes:
        UUID (uuid.UUID): A unique identifier for this instance.
        USER (str): The user the process should run as.
        DEBUG (bool): Whether to enable debug mode.
        LOG_FILE (str): The path to the log file.
        LOG_LEVEL (str): logging level.
        PUBLISH_AMI_EVENTS (bool): Whether to publish AMI events to the message bus.
        ami (AMISettings): Settings for the AMI client.
        ajam (AJAMSettings): Settings for the AJAM client.
        auth (AuthSettings): Settings for the authentication client.
        bus (BusSettings): Settings for the message bus.
        rest_api (RestApiSettings): Settings for the REST API.

    """

    UUID: uuid.UUID = Field(default_factory=uuid.uuid4)
    USER: str = "accent-amid"
    DEBUG: bool = False
    LOG_FILE: str = "/var/log/accent-amid.log"
    LOG_LEVEL: str = "INFO"
    PUBLISH_AMI_EVENTS: bool = True

    ami: AMISettings = AMISettings()
    ajam: AJAMSettings = AJAMSettings()
    auth: AuthSettings = AuthSettings()
    bus: BusSettings = BusSettings()
    rest_api: RestApiSettings = RestApiSettings()

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_log_level(self) -> int:
        """Converts string log level to numeric.

        Returns:
            int: logging level, as a number.

        """  # noqa: D401
        level_mapping = logging.getLevelNamesMapping()
        log_level = self.LOG_LEVEL.upper()
        if log_level in level_mapping:
            return level_mapping[log_level]  # type: ignore[return-value]
        return logging.INFO  # Default level.
