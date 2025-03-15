# src/accent_chatd/main.py
import asyncio
import logging.config

import uvicorn
from fastapi import FastAPI, HTTPException

from accent_chatd.api.common import common_router
from accent_chatd.api.config.routes import config_router
from accent_chatd.api.presences.routes import presence_router
from accent_chatd.api.rooms.routes import room_router
from accent_chatd.api.status.routes import status_router
from accent_chatd.api.teams_presence.routes import teams_router
from accent_chatd.core.bus import get_bus_consumer
from accent_chatd.core.config import get_settings
from accent_chatd.core.database import Base, engine
from accent_chatd.core.exceptions import http_exception_handler
from accent_chatd.core.middleware import ExampleMiddleware

settings = get_settings()
# Configure logging
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="accent-chatd",
    description="REST API for managing chat presence and messages.",
    version="1.0.0",  # Replace with your actual version
    docs_url="/docs",  # Make Swagger UI available at /docs
    redoc_url=None,  # Disable ReDoc
    openapi_url="/openapi.json",  # Serve OpenAPI spec at /openapi.json
)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)

# Add middleware
app.add_middleware(ExampleMiddleware)

# Include routers for different API resources
app.include_router(common_router)
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(presence_router, prefix="/users", tags=["presences"])
app.include_router(room_router, prefix="/users", tags=["rooms", "messages"])
app.include_router(status_router, prefix="/status", tags=["status"])
app.include_router(teams_router, prefix="/users", tags=["teams_presence"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    # Create database tables (using Alembic is preferred for migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Initialize any background tasks, connect to the bus, etc.
    logger.info("Startup complete.")

    # Connect to bus.
    bus_consumer = await get_bus_consumer()
    await bus_consumer.connect()
    asyncio.create_task(bus_consumer.run())  # Create task to run.


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    # Gracefully close connections, stop background tasks, etc.
    bus_consumer = await get_bus_consumer()
    if bus_consumer:
        await bus_consumer.disconnect()  # Disconnect
        bus_consumer.stop()  # Stop running.
    await engine.dispose()
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
