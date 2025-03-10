# Copyright 2025 Accent Communications

"""Test fixtures for accent-lib-rest-client."""

import asyncio
import logging
import os
import sys
from typing import Any, AsyncGenerator, Generator

import httpx
import pytest
import respx
import uvicorn
from fastapi import FastAPI
from pytest_mock import MockerFixture

from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.command import RESTCommand
from tests.mock_server.server import create_app


# Basic fixture for REST command testing
class TestCommand(RESTCommand):
    """Test command implementation."""

    resource = "test"

    def get_data(self) -> dict[str, Any]:
        """Get test data."""
        response = self.sync_client.get(f"{self.base_url}/data")
        response.raise_for_status()
        return response.json()

    async def get_data_async(self) -> dict[str, Any]:
        """Get test data asynchronously."""
        response = await self.async_client.get(f"{self.base_url}/data")
        response.raise_for_status()
        return response.json()


# Basic client for testing
class TestClient(BaseClient):
    """Test client implementation."""

    namespace = "test_client.commands"

def pytest_configure(config):
    """Configure pytest."""
    # Set the default asyncio fixture loop scope explicitly
    config.option.asyncio_default_fixture_loop_scope = "function"

@pytest.fixture
def test_command_class() -> type[TestCommand]:
    """Return the test command class."""
    return TestCommand


@pytest.fixture
def test_client() -> TestClient:
    """Return a test client instance."""
    return TestClient(
        host="localhost",
        port=8000,
        version="v1",
        https=False,
    )


@pytest.fixture
def mock_response() -> dict[str, Any]:
    """Return a mock response body."""
    return {"data": "test value", "status": "success"}


@pytest.fixture
def respx_mock() -> respx.Router:
    """Return a respx mock router."""
    with respx.mock(base_url="http://localhost:8000") as mock:
        yield mock


@pytest.fixture
def httpx_mock(respx_mock: respx.Router) -> respx.Router:
    """Return a configured respx mock with common patterns."""
    # Set up common routes
    respx_mock.get("/v1/test/data").respond(
        json={"data": "test value", "status": "success"}
    )
    respx_mock.post("/v1/test/create").respond(
        json={"id": "new-item", "status": "created"}, status_code=201
    )
    respx_mock.get("/v1/not-found").respond(status_code=404)
    respx_mock.get("/v1/error").respond(status_code=500)
    respx_mock.get("/v1/auth").respond(status_code=401)

    return respx_mock


@pytest.fixture(scope="session")
def mock_server_app() -> FastAPI:
    """Create and return the FastAPI mock server app."""
    return create_app()


@pytest.fixture(scope="session")
def mock_server(mock_server_app: FastAPI) -> Generator[None, None, None]:
    """Start the FastAPI mock server in a separate process."""
    # Disable server logs during tests
    logging.getLogger("uvicorn").setLevel(logging.WARNING)

    # Start the server in a separate process
    port = 8000
    config = uvicorn.Config(
        mock_server_app, host="127.0.0.1", port=port, log_level="error"
    )
    server = uvicorn.Server(config)

    # Run the server in a separate thread
    import threading

    thread = threading.Thread(target=server.run)
    thread.daemon = True
    thread.start()

    # Wait for server to start
    import time

    time.sleep(1)

    yield

    # Server will automatically shut down when the process exits


@pytest.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Return an async client for testing."""
    async with httpx.AsyncClient() as client:
        yield client
