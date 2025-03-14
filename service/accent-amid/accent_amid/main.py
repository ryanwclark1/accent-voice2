# src/accent_amid/main.py
from __future__ import annotations

import logging
import signal
from contextlib import asynccontextmanager
from functools import partial
from typing import TYPE_CHECKING

from accent_auth_client import Client as AuthClient
from accent_bus.publisher import BusPublisherWithQueue
from fastapi import FastAPI

from accent_amid.api import actions, api, commands, config, status
from accent_amid.config import Settings
from accent_amid.controller import Controller
from accent_amid.database import engine
from accent_amid.utils.logging import setup_logging

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from types import FrameType

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle startup and shutdown events for the application using lifespan.

    This function is called when the application starts up and shuts down.
    It initializes and closes the database connection pool, and closes the bus.

    Args:
        app (FastAPI): fastAPI application.

    Yields:
        None

    """
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
    """Create the FastAPI application instance.

    This function initializes the FastAPI app, sets up logging, includes API routers,
    and optionally sets up database connections and other dependencies.

    Args:
        settings (Settings | None): The settings object to use. Defaults to a new Settings instance.
        bus_client (BusPublisherWithQueue, optional): a bus client.
        auth_client (AuthClient, optional): an accent auth client.

    Returns:
        FastAPI: The initialized FastAPI application.

    """
    _settings = settings or Settings()
    setup_logging(_settings.LOG_FILE, _settings.DEBUG)

    app = FastAPI(
        title="Accent AMI Daemon",
        description="A modern daemon for interacting with Asterisk's AMI, built with FastAPI.",
        version="0.2.0",  # Updated version
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

    # Store settings and other dependencies in app state for access by endpoints
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


def run_app() -> None:
    """Run the application using the configured settings.

    This function sets up the controller, handles signals, and runs the main loop.
    """
    settings = Settings()

    controller = Controller(settings)
    signal.signal(signal.SIGTERM, partial(_signal_handler, controller))
    signal.signal(signal.SIGINT, partial(_signal_handler, controller))
    controller.run()


def _signal_handler(controller: Controller, signum: int, frame: FrameType) -> None:
    """Handle system signals to gracefully stop the application.

    Args:
        controller (Controller): The application's controller.
        signum (int): The signal number.
        frame (FrameType): The current stack frame.

    """
    controller.stop(reason=signal.Signals(signum).name)
