# src/accent_amid/main.py
from __future__ import annotations

import asyncio
import logging
import signal
from contextlib import asynccontextmanager
from functools import partial
from typing import TYPE_CHECKING

from accent_auth_client import Client as AuthClient
from accent_bus.publisher import BusPublisherWithQueue
from fastapi import FastAPI

from accent_amid.api import actions, api, commands, config, status
from accent_amid.auth import init_master_tenant
from accent_amid.config import Settings

# REMOVE: from accent_amid.controller import Controller
from accent_amid.database import engine
from accent_amid.services.ami import AMIService  # Keep this import
from accent_amid.utils.logging import setup_logging

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from types import FrameType

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage the lifespan of the FastAPI application.

    This function is an asynchronous context manager that handles the startup
    and shutdown events of the FastAPI application. It initializes the database
    connection pool on startup and closes the connections on shutdown. Additionally,
    it closes the bus client connection if it exists in the application state.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function does not yield any values.

    """
    # ... (lifespan remains the same)
    logger.info("Starting up...")
    await engine.connect()  # Initialize the database connection pool
    yield
    logger.info("Shutting down...")
    await engine.dispose()  # Close database connections
    if hasattr(app.state, "bus_client"):
        await app.state.bus_client.close_connection()
        logger.info("Bus client connection closed.")


def create_app(
    settings: Settings | None = None,
    bus_client: BusPublisherWithQueue | None = None,
    auth_client: AuthClient | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings (Settings | None): Optional settings object. If not provided, a default
        Settings instance is used.
        bus_client (BusPublisherWithQueue | None): Optional bus client for publishing
            messages. If not provided, a default BusPublisherWithQueue
            instance is created.
        auth_client (AuthClient | None): Optional authentication client.
            If not provided, a default AuthClient instance is created.

    Returns:
        FastAPI: The configured FastAPI application instance.

    """
    _settings = settings or Settings()
    setup_logging(_settings.LOG_FILE, _settings.DEBUG)

    app = FastAPI(
        title="Accent AMI Daemon",
        description="A modern daemon for interacting with Asterisk's AMI, built with FastAPI.",
        version="0.2.0",
        openapi_tags=[
            {"name": "actions", "description": "Operations related to AMI actions."},
            {"name": "commands", "description": "Executing AMI commands."},
            {"name": "config", "description": "Managing service configuration."},
            {"name": "status", "description": "Service status checks."},
        ],
        lifespan=lifespan,
    )

    # Include API routers
    app.include_router(actions.router, prefix="/actions", tags=["actions"])
    app.include_router(commands.router, prefix="/commands", tags=["commands"])
    app.include_router(config.router, prefix="/config", tags=["config"])
    app.include_router(status.router, prefix="/status", tags=["status"])
    app.include_router(api.router, prefix="", tags=["api"])

    # Store settings and other dependencies in app state
    app.state.settings = _settings
    app.state.bus_client = (
        bus_client
        if bus_client
        else BusPublisherWithQueue(
            name="accent-amid",
            service_uuid=str(_settings.UUID),
            **_settings.bus.model_dump(),
        )
    )
    app.state.auth_client = (
        auth_client if auth_client else AuthClient(**_settings.auth.model_dump())
    )

    return app


async def run_app_async() -> None:  # New async run_app
    """Run the application using the configured settings.

    This function sets up the controller, handles signals, and runs the main loop.
    """
    settings = Settings()
    bus_client = BusPublisherWithQueue(
        name="accent-amid", service_uuid=str(settings.UUID), **settings.bus.model_dump()
    )
    auth_client = AuthClient(**settings.auth.model_dump())

    ami_service = AMIService(settings, bus_client, auth_client)
    # Set up signal handling (using partial to pass ami_service)
    signal.signal(signal.SIGTERM, partial(_signal_handler, ami_service))
    signal.signal(signal.SIGINT, partial(_signal_handler, ami_service))

    await init_master_tenant(auth_client, settings)
    async with ami_service:  # Use async context manager
        if settings.PUBLISH_AMI_EVENTS:
            await ami_service.run()


def run_app() -> None:
    """Sync entry point that runs the async `run_app_async`."""
    asyncio.run(run_app_async())


async def _signal_handler(
    ami_service: AMIService, signum: int, frame: FrameType
) -> None:  # Now takes AMIService
    """Handle system signals."""
    logger.warning("Stopping accent-amid: %s", signal.Signals(signum).name)
    await ami_service.stop()  # Use await, as stop is async
