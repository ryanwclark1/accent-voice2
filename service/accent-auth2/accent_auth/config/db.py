# accent_auth/config/db.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    db_uri: str = "postgresql+asyncpg://asterisk:password123@localhost/asterisk"
    db_connect_retry_timeout_seconds: int = 300
    db_upgrade_on_startup: bool = False
    db_pool_size: int = 16  # Example value
    db_max_overflow: int = 0  # Example value
    model_config = SettingsConfigDict(env_prefix="accent_auth_", frozen=False)


settings = DatabaseSettings()
