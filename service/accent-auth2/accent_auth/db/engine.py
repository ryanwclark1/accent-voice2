# accent_auth/db/engine.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from accent_auth.config.db import settings as db_settings

# Create async database engine with connection pooling
async_engine = create_async_engine(
    db_settings.db_uri,
    pool_size=db_settings.db_pool_size,
    max_overflow=db_settings.db_max_overflow,
    echo=db_settings.db_echo,  # Use the configured echo setting
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
