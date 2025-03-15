# src/accent_chatd/main.py
import asyncio
import logging.config

import uvicorn
from fastapi import FastAPI, HTTPException
from accent_chatd.core.config import get_settings
from accent_chatd.core.database import Base, engine
from accent_chatd.core.exceptions import http_exception_handler

# from accent_chatd.services.teams import TeamsService  # No longer needed at top-level
from accent_chatd.core.middleware import ExampleMiddleware
from accent_chatd.core.bus import get_bus_consumer, get_bus_publisher
from accent_chatd.api.common import common_router
from accent_chatd.core.plugin import Plugin  # Import the Plugin base class
from accent_chatd.dao import DAO

# Import plugin modules.  These imports *must* be here, after the
# FastAPI app is created, because the plugin modules depend on `app`.
from accent_chatd.plugins.config.plugin import Plugin as ConfigPlugin
from accent_chatd.plugins.presences.plugin import Plugin as PresencesPlugin
from accent_chatd.plugins.rooms.plugin import Plugin as RoomsPlugin
from accent_chatd.plugins.status.plugin import Plugin as StatusPlugin
from accent_chatd.plugins.api.plugin import Plugin as ApiPlugin
from accent_chatd.plugins.teams_presence.plugin import Plugin as TeamsPresencePlugin

settings = get_settings()
# Configure logging
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="accent-chatd",
    description="REST API for managing chat presence and messages.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_middleware(ExampleMiddleware)  # Add middleware

# --- Plugin Registration ---
# List of plugins to load.  Order matters here; if plugins depend on each
# other, the dependencies need to be loaded *before* the dependents.
plugins: List[Plugin] = [
    ApiPlugin(),
    ConfigPlugin(),
    StatusPlugin(),
    PresencesPlugin(),
    RoomsPlugin(),
    TeamsPresencePlugin(),  # Load last, as it uses many other items.
]


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    # Create database tables (using Alembic is preferred for migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Initialize any background tasks, connect to the bus, etc.
    logger.info("Startup complete.")

    # Start the bus consumer in a separate thread
    bus_consumer = await get_bus_consumer()
    await bus_consumer.connect()
    asyncio.create_task(bus_consumer.run())  # use asyncio.

    # --- Plugin Loading ---
    # Create a dictionary of dependencies to pass to plugins
    dependencies = {
        "app": app,
        "config": settings,
        "bus_consumer": bus_consumer,
        "bus_publisher": await get_bus_publisher(),
        "dao": DAO(),  # Pass the DAO
        # Add other dependencies as needed
    }

    for plugin in plugins:
        try:
            plugin.load(dependencies)
            logger.info(f"Loaded plugin: {type(plugin).__name__}")
        except Exception:
            logger.exception(f"Failed to load plugin: {type(plugin).__name__}")
            raise  # Re-raise to halt startup if a plugin fails


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    # Gracefully close connections, stop background tasks, etc.
    bus_consumer = await get_bus_consumer()
    if bus_consumer:
        await bus_consumer.disconnect()  # Disconnect
        bus_consumer.stop()  # Stop running.
    await engine.dispose()
    # get_aio_core().stop() # No longer needed.
    logger.info("Shutdown complete.")


# Create a dummy endpoint at the root for health checks
@app.get("/")
async def root():
    return {"message": "accent-chatd is running"}


def main():
    """Entrypoint for running the server with Uvicorn."""
    uvicorn.run(
        "accent_chatd.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
