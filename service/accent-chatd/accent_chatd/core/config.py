# src/accent_chatd/core/config.py
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    PostgresDsn,
    Field,
    ValidationError,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from yaml import safe_load

# Helper function to load YAML config
def load_yaml_config_settings_source(file_path: str | Path) -> dict[str, Any]:
    """Load settings from a YAML file."""
    path = Path(file_path)
    if not path.exists():
       return {}
    
    with path.open("r") as f:
        return safe_load(f)

class CorsSettings(BaseModel):
    enabled: bool = True
    allow_headers: List[str] = [
        "Content-Type",
        "X-Auth-Token",
        "Accent-Tenant",
    ]
    allow_origins: List[str] = ["*"]  # Default to allow all origins
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]  # Default to allow all methods
    expose_headers: List[str] = []
    max_age: int = 600

class RestApiSettings(BaseModel):
    listen: str = "127.0.0.1"
    port: int = 9304
    cors: CorsSettings = Field(default_factory=CorsSettings)
    max_threads: int = 10

class AuthSettings(BaseModel):
    host: str = "localhost"
    port: int = 9497
    prefix: Optional[str] = None
    https: bool = False
    key_file: str = "/var/lib/accent-auth-keys/accent-chatd-key.yml"
    username: Optional[str] = None  # Will be populated from key_file
    password: Optional[str] = None  # Will be populated from key_file

class AmidSettings(BaseModel):
    host: str = "localhost"
    port: int = 9491
    prefix: Optional[str] = None
    https: bool = False

class ConfdSettings(BaseModel):
    host: str = "localhost"
    port: int = 9486
    prefix: Optional[str] = None
    https: bool = False
    timeout: int = 30

class BusSettings(BaseModel):
    username: str = "guest"
    password: str = "guest"
    host: str = "localhost"
    port: int = 5672
    exchange_name: str = "accent-headers"
    exchange_type: str = "headers"

class ConsulSettings(BaseModel):
    scheme: str = "http"
    port: int = 8500
    host: str = 'localhost'

class ServiceDiscoverySettings(BaseModel):
    enabled: bool = False
    advertise_address: str = "auto"
    advertise_address_interface: str = "eth0"
    advertise_port: int = 9304
    ttl_interval: int = 30
    refresh_interval: int = 27
    retry_interval: int = 2
    extra_tags: List[str] = []

class EnabledPlugins(BaseModel):
    api: bool = True
    config: bool = True
    presences: bool = True
    rooms: bool = True
    status: bool = True
    teams_presence: bool = False

class InitializationSettings(BaseModel):
    enabled: bool = True

class TeamsPresenceSettings(BaseModel):
    microsoft_graph_url: str = "https://graph.microsoft.com/v1.0"

class Settings(BaseSettings):
    # Main Configuration
    config_file: str = "/etc/accent-chatd/config.yml"
    debug: bool = False
    extra_config_files: str = "/etc/accent-chatd/conf.d"
    log_file: str = "/var/log/accent-chatd.log"
    log_level: str = "info"
    user: str = "accent-chatd"
    # Component Settings, using nested models
    rest_api: RestApiSettings = Field(default_factory=RestApiSettings)
    db_uri: PostgresDsn = "postgresql://asterisk:password123@localhost/asterisk?application_name=accent-chatd"
    auth: AuthSettings = Field(default_factory=AuthSettings)
    amid: AmidSettings = Field(default_factory=AmidSettings)
    confd: ConfdSettings = Field(default_factory=ConfdSettings)
    bus: BusSettings = Field(default_factory=BusSettings)
    consul: ConsulSettings = Field(default_factory=ConsulSettings)
    service_discovery: ServiceDiscoverySettings = Field(default_factory=ServiceDiscoverySettings)
    enabled_plugins: EnabledPlugins = Field(default_factory=EnabledPlugins)
    initialization: InitializationSettings = Field(default_factory=InitializationSettings)
    teams_presence: TeamsPresenceSettings = Field(default_factory=TeamsPresenceSettings)

    # new field
    service_id: str = ""
    service_key: str = ""
    # can be a uuid
    uuid: str = ""

    host: str = Field(default="0.0.0.0", validation_alias="rest_api.listen")
    port: int = Field(default=9304, validation_alias="rest_api.port")
    db_echo: bool = Field(default=False, validation_alias="debug")

    model_config = SettingsConfigDict(
        env_prefix="",  # No prefix for environment variables
        extra="allow",  # Allow extra fields (for merging configs)
        frozen=False,   # Allow the Settings to be changed.
        validate_assignment=True # validate on assignment.
    )

    @field_validator('log_level')
    def log_level_validator(cls, v):
        if isinstance(v, str):
          v = v.upper()
          if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
              raise ValueError("Invalid log level")
        return v
    
    @field_validator("db_uri", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return v
    
    def load_extra_config_files(self) -> None:
        """Loads extra configuration files from the specified directory."""
        if not self.extra_config_files:
            return

        extra_config_path = Path(self.extra_config_files)
        if not extra_config_path.is_dir():
            # logger.warning(f"Extra config directory '{self.extra_config_files}' does not exist.")
            return

        # Sort the files to load them in a consistent order (e.g., lexicographically)
        config_files = sorted(extra_config_path.glob("*.yml")) + sorted(
            extra_config_path.glob("*.yaml")
        )

        for config_file in config_files:
            # logger.info(f"Loading extra config file: {config_file}")
            try:
                extra_settings = load_yaml_config_settings_source(config_file)
                # The settings object allows direct updates.
                for key, value in extra_settings.items():
                    if hasattr(self, key):
                         # Check for nested model.
                        if isinstance(getattr(self, key), BaseModel):
                            # Use model_copy(update=)
                            updated_model = getattr(self,key).model_copy(update=value)
                            setattr(self, key, updated_model)
                        else:
                            setattr(self, key, value)
                    else:
                        setattr(self, key, value)

            except (OSError, ValidationError) as e:
                # logger.error(f"Error loading extra config file '{config_file}': {e}")
                pass    

    def load_key_file(self) -> None:
      # Load service key and id.
      key_file_settings = load_yaml_config_settings_source(self.auth.key_file)

      if key_file_settings and 'service_id' in key_file_settings and 'service_key' in key_file_settings:
          self.service_id = key_file_settings["service_id"]
          self.service_key = key_file_settings["service_key"]


@lru_cache()
def get_settings():
    # Use lru_cache to avoid reloading settings multiple times
    settings = Settings()
    settings.load_extra_config_files()
    settings.load_key_file()
    return settings