# src/accent_chatd/core/dependencies.py

from accent_chatd.core.config import get_settings, Settings
from sqlalchemy.ext.asyncio import AsyncSession
from accent_chatd.core.database import get_async_session
# Add any other dependencies that you may need.


# Dependency to get the config settings
def get_config() -> Settings:
    return get_settings()
