import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_target_metadata():
    from accent_chatd.database import models

    return models.Base.metadata


VERSION_TABLE = 'chatd_alembic_version'
URI = os.getenv('ALEMBIC_DB_URI', None)


def get_url():
    # The import should not be top level to allow the usage of the ALEMBIC_DB_URI
    # environment variable when the DB is not hosted on the same host as accent-chatd.
    # When building the docker image for the database for example.

    chatd_config = load_config('')
    return chatd_config.get('db_uri')


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = URI or config.get_main_option("sqlalchemy.url") or get_url()
    context.configure(url=url, version_table=VERSION_TABLE)

    with context.begin_transaction():
        context.run_migrations()


# alembic/env.py
def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    from accent_chatd.core.config import get_settings

    settings = get_settings()  # Get the settings

    connectable = create_async_engine(
        settings.db_uri.replace("postgresql://", "postgresql+asyncpg://", 1),
        future=True,
    )

    async def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=get_target_metadata(),
            version_table=VERSION_TABLE,  # Use your version table name
        )
        async with context.begin_transaction():
            await context.run_migrations()

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    asyncio.run(run_async_migrations())
