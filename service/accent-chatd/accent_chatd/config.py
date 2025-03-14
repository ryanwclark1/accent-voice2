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
    service_id: str = Field(..., alias="auth.username")
    service_key: str = Field(..., alias="auth.password")
    # can be a uuid
    uuid: str = ""

    model_config = SettingsConfigDict(
        env_prefix="",  # No prefix for environment variables
        