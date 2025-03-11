# Copyright 2025 Accent Communications
"""Configuration for the Accent applicationd client.
"""

from __future__ import annotations

import copy
import logging
from typing import Any, ClassVar

import httpx

from accent_applicationd_client.exceptions import ApiValueError
from accent_applicationd_client.models.settings import Settings

# Configure logger
logger = logging.getLogger(__name__)

# JSON schema validation keywords
JSON_SCHEMA_VALIDATION_KEYWORDS: set[str] = {
    "multipleOf",
    "maximum",
    "exclusiveMaximum",
    "minimum",
    "exclusiveMinimum",
    "maxLength",
    "minLength",
    "pattern",
    "maxItems",
    "minItems",
}


class Configuration:
    """Configuration for the API client.

    This class manages client configuration such as authentication, server settings,
    and request validation.

    Attributes:
        host: Base URL for API requests
        api_key: Dictionary of API keys for authentication
        api_key_prefix: Dictionary of API key prefixes
        username: Username for HTTP basic authentication
        password: Password for HTTP basic authentication
        discard_unknown_keys: Whether to discard unknown properties
        disabled_client_side_validations: Comma-separated validation rules to skip
        server_index: Index to server configuration
        server_variables: Mapping for templated server config
        server_operation_index: Operation ID to server config index
        server_operation_variables: Operation ID to server config variables
        temp_folder_path: Folder for downloads
        logger: Dictionary of loggers
        logger_format: Log format string
        debug: Debug logging flag
        verify_ssl: Whether to verify SSL certificates
        ssl_ca_cert: Custom certificate authority bundle
        cert_file: Client certificate file
        key_file: Client key file
        connection_pool_maxsize: Maximum connections per pool
        proxy: Proxy URL
        proxy_headers: Headers for proxy requests
        safe_chars_for_path_param: Characters to not encode in path parameters
        retries: Request retry configuration
        client_side_validation: Whether to validate client-side

    """

    _default: ClassVar[Configuration | None] = None

    def __init__(
        self,
        host: str | None = None,
        api_key: dict[str, str] | None = None,
        api_key_prefix: dict[str, str] | None = None,
        username: str | None = None,
        password: str | None = None,
        discard_unknown_keys: bool = False,
        disabled_client_side_validations: str = "",
        server_index: int | None = None,
        server_variables: dict[str, str] | None = None,
        server_operation_index: dict[str, int] | None = None,
        server_operation_variables: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """Initialize configuration.

        Args:
            host: Base URL for API requests
            api_key: Dictionary of API keys for authentication
            api_key_prefix: Dictionary of API key prefixes
            username: Username for HTTP basic authentication
            password: Password for HTTP basic authentication
            discard_unknown_keys: Whether to discard unknown properties
            disabled_client_side_validations: Comma-separated validation rules to skip
            server_index: Index to server configuration
            server_variables: Mapping for templated server config
            server_operation_index: Operation ID to server config index
            server_operation_variables: Operation ID to server config variables

        """
        self._base_path = "http://localhost" if host is None else host
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}

        # Path for temporary files
        self.temp_folder_path: str | None = None

        # Authentication settings
        self.api_key = {}
        if api_key:
            self.api_key = api_key

        self.api_key_prefix = {}
        if api_key_prefix:
            self.api_key_prefix = api_key_prefix

        self.refresh_api_key_hook = None
        self.username = username
        self.password = password
        self.discard_unknown_keys = discard_unknown_keys
        self.disabled_client_side_validations = disabled_client_side_validations

        # Logging settings
        self.logger: dict[str, logging.Logger] = {
            "package_logger": logging.getLogger("accent_applicationd_client"),
            "httpx_logger": logging.getLogger("httpx"),
        }
        self.logger_format = "%(asctime)s %(levelname)s %(message)s"
        self.logger_stream_handler = None
        self.logger_file_handler = None
        self.logger_file: str | None = None
        self.debug = False

        # SSL/TLS settings
        self.verify_ssl = True
        self.ssl_ca_cert: str | None = None
        self.cert_file: str | None = None
        self.key_file: str | None = None

        # Connection settings
        self.connection_pool_maxsize = 10
        self.proxy: str | None = None
        self.proxy_headers: dict[str, str] | None = None
        self.safe_chars_for_path_param = ""
        self.retries: httpx.Limits | None = None

        # Enable client side validation by default
        self.client_side_validation = True

        # Create the settings object for easy access
        self.settings = Settings(
            host=self._base_path,
            api_key=self.api_key,
            api_key_prefix=self.api_key_prefix,
            username=self.username,
            password=self.password,
            verify_ssl=self.verify_ssl,
            ssl_ca_cert=self.ssl_ca_cert,
            cert_file=self.cert_file,
            key_file=self.key_file,
            connection_pool_maxsize=self.connection_pool_maxsize,
            proxy=self.proxy,
            proxy_headers=self.proxy_headers,
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> Configuration:
        """Create a deep copy of the configuration.

        Args:
            memo: Dictionary for memoization

        Returns:
            A deep copy of this configuration

        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if k not in ("logger", "logger_file_handler"):
                setattr(result, k, copy.deepcopy(v, memo))

        # Shallow copy of loggers
        result.logger = copy.copy(self.logger)

        # Use setters to configure loggers
        result.logger_file = self.logger_file
        result.debug = self.debug

        return result

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute with validation for disabled validations.

        Args:
            name: Attribute name
            value: Attribute value

        Raises:
            ApiValueError: If an invalid validation keyword is provided

        """
        object.__setattr__(self, name, value)

        if name == "disabled_client_side_validations":
            s = set(filter(None, value.split(",")))
            for v in s:
                if v not in JSON_SCHEMA_VALIDATION_KEYWORDS:
                    raise ApiValueError(f"Invalid keyword: '{v}'")
            self._disabled_client_side_validations = s

    @classmethod
    def set_default(cls, default: Configuration) -> None:
        """Set default instance of configuration.

        It stores default configuration, which can be
        returned by get_default_copy method.

        Args:
            default: Configuration object to use as default

        """
        cls._default = copy.deepcopy(default)

    @classmethod
    def get_default_copy(cls) -> Configuration:
        """Return new instance of configuration.

        This method returns a newly created configuration instance
        or a copy of the default configuration.

        Returns:
            A configuration object

        """
        if cls._default is not None:
            return copy.deepcopy(cls._default)

        return Configuration()

    @property
    def logger_file(self) -> str | None:
        """Get the logger file path.

        Returns:
            Path to the logger file or None

        """
        return self.__logger_file if hasattr(self, "__logger_file") else None

    @logger_file.setter
    def logger_file(self, value: str | None) -> None:
        """Set the logger file.

        If the logger_file is None, add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        Args:
            value: The logger file path

        """
        self.__logger_file = value
        if self.__logger_file:
            # If setting logging file, add file handler and remove stream handler
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)

            for _, logger in self.logger.items():
                logger.addHandler(self.logger_file_handler)

    @property
    def debug(self) -> bool:
        """Get debug status.

        Returns:
            Debug status flag

        """
        return self.__debug if hasattr(self, "__debug") else False

    @debug.setter
    def debug(self, value: bool) -> None:
        """Set debug status.

        Args:
            value: Debug status (True or False)

        """
        self.__debug = value
        if self.__debug:
            # If debug is True, enable debug logging
            for _, logger in self.logger.items():
                logger.setLevel(logging.DEBUG)
        else:
            # If debug is False, set level to warning
            for _, logger in self.logger.items():
                logger.setLevel(logging.WARNING)

    @property
    def logger_format(self) -> str:
        """Get the logger format.

        Returns:
            Logger format string

        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value: str) -> None:
        """Set the logger format and update formatter.

        Args:
            value: Format string

        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(
        self, identifier: str, alias: str | None = None
    ) -> str | None:
        """Get API key with optional prefix.

        Args:
            identifier: The identifier of the API key
            alias: Alternative identifier for the API key

        Returns:
            API key with prefix if set, or None if no key exists

        """
        if self.refresh_api_key_hook is not None:
            self.refresh_api_key_hook(self)

        key = self.api_key.get(
            identifier, self.api_key.get(alias) if alias is not None else None
        )
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return f"{prefix} {key}"
            return key

        return None

    def get_basic_auth_token(self) -> str | None:
        """Get HTTP basic authentication header.

        Returns:
            Basic auth token string or None if not configured

        """
        if self.username is None or self.password is None:
            return None

        credentials = f"{self.username}:{self.password}"
        return httpx.BasicAuth(self.username, self.password).auth_header_value

    def auth_settings(self) -> dict[str, dict[str, Any]]:
        """Get authentication settings.

        Returns:
            Dictionary of auth settings

        """
        # This application has no auth settings in the example
        return {}

    def to_debug_report(self) -> str:
        """Generate debugging information.

        Returns:
            Debug report as a string

        """
        import platform
        import sys

        return (
            "Python SDK Debug Report:\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Python Version: {sys.version}\n"
            "API Version: 0.1.0\n"
            "SDK Package Version: 2.0.0"
        )

    def get_host_settings(self) -> list[dict[str, str]]:
        """Get host settings.

        Returns:
            List of host settings

        """
        return [
            {
                "url": "/",
                "description": "Default server",
            }
        ]

    def get_host_from_settings(
        self,
        index: int | None,
        variables: dict[str, str] | None = None,
        servers: list[dict[str, Any]] | None = None,
    ) -> str:
        """Build host URL from settings.

        Args:
            index: Array index of host settings
            variables: Dictionary of variables and values
            servers: List of server settings

        Returns:
            Host URL

        Raises:
            ValueError: If index is invalid

        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                f"Invalid index {index} when selecting the host settings. "
                f"Must be less than {len(servers)}"
            )

        url = server["url"]

        # Replace variable placeholders
        for variable_name, variable in server.get("variables", {}).items():
            used_value = variables.get(variable_name, variable["default_value"])

            if "enum_values" in variable and used_value not in variable["enum_values"]:
                raise ValueError(
                    f"The variable `{variable_name}` in the host URL has invalid value "
                    f"{variables[variable_name]}. Must be {variable['enum_values']}."
                )

            url = url.replace(f"{{{variable_name}}}", used_value)

        return url

    @property
    def host(self) -> str:
        """Get the host URL.

        Returns:
            Host URL

        """
        return self.get_host_from_settings(
            self.server_index, variables=self.server_variables
        )

    @host.setter
    def host(self, value: str) -> None:
        """Set the host URL.

        Args:
            value: Host URL

        """
        self._base_path = value
        self.server_index = None
