# Copyright 2025 Accent Communications

import asyncio
import threading
from typing import Any, Dict, Generator

import httpx
import pytest
import respx
from accent_lib_rest_client.tests.conf import mock_request
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, HTTPException

from accent_amid_client.client import AmidClient


# --- Mock Server Setup ---
def create_app() -> FastAPI:
    """Creates the FastAPI application for mocking."""
    app = FastAPI()

    # --- Status Endpoint ---
    @app.get("/api/amid/status")
    async def mock_status():
        return {"status": "OK"}

    # --- Config Endpoint ---
    @app.get("/api/amid/config")
    async def mock_config_get():
        return {"setting1": "value1", "setting2": "value2"}

    @app.patch("/api/amid/config")
    async def mock_config_patch(updated_config: Dict[str, Any]):
        # In a real mock, you'd likely update a stored config
        return {**{"setting1": "value1", "setting2": "value2"}, **updated_config}

    # --- Action Endpoint ---
    @app.post("/api/amid/action/{action_name}")
    async def mock_action(action_name: str, params: Dict[str, Any] | None = None):
        if action_name == "QueueSummary":
            return [{"Response": "Success", "Queue": "support", "Members": 1}]
        elif action_name == "DBGet":
            if params and params.get("Family") == "testfamily":
                return [{"Response": "Success", "Value": "testvalue"}]
            else:
                return [
                    {"Response": "Error", "Message": "DBGet failed"}
                ]  # Example of a protocol error
        raise HTTPException(status_code=404, detail="Action not found")

    # --- Command Endpoint ---
    @app.post("/api/amid/action/Command")
    async def mock_command(command_data: Dict[str, str]):
        command = command_data.get("command")
        if command == "core show channels":
            return {"output": "Channels: 1 active"}
        else:
            raise HTTPException(
                status_code=400, detail="Invalid command"
            )  # Simulate bad request

    # --- Error Simulation ---
    @app.get("/api/amid/error_503")
    async def mock_error_503():
        raise HTTPException(status_code=503, detail="Service Unavailable")

    @app.get("/api/amid/error_400")
    async def mock_error_400():
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Bad Request",
                "error_id": "ID123",
                "details": "Invalid input",
                "timestamp": "2024-07-30T12:00:00Z",
            },
        )

    return app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Provides the FastAPI application instance."""
    return create_app()


@pytest.fixture(scope="session")
async def mock_server(app: FastAPI) -> str:
    """Starts the mock server and returns its URL."""
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/amid/status")  # Check server is up
            assert response.status_code == 200
        yield "http://test"  # Use a fixed URL, not a dynamic port.


@pytest.fixture
def httpx_mock() -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock router for httpx requests."""
    with respx.mock(assert_all_called=False) as respx_mock:
        yield respx_mock


@pytest.fixture
def mock_client(mock_server: str) -> AmidClient:
    """Provides an instance of the AmidClient pointed to the mock server."""
    return AmidClient(host=mock_server, port=80)  # Use port 80 for the mock server


@pytest.fixture
def mock_503_response(httpx_mock: respx.MockRouter, mock_server: str):
    httpx_mock.get(f"{mock_server}/api/amid/status").mock(
        return_value=httpx.Response(503)
    )


@pytest.fixture
def mock_400_response(httpx_mock: respx.MockRouter, mock_server: str):
    httpx_mock.get(f"{mock_server}/api/amid/status").mock(
        return_value=httpx.Response(
            400,
            json={
                "message": "Bad Request",
                "error_id": "ID123",
                "details": "Invalid input",
                "timestamp": "2024-07-30T12:00:00Z",
            },
        )
    )


@pytest.fixture
def mock_invalid_json_response(httpx_mock: respx.MockRouter, mock_server: str):
    httpx_mock.get(f"{mock_server}/api/amid/status").mock(
        return_value=httpx.Response(200, content="invalid json")
    )


@pytest.fixture
def mock_invalid_amid_response(httpx_mock: respx.MockRouter, mock_server: str):
    httpx_mock.get(f"{mock_server}/api/amid/status").mock(
        return_value=httpx.Response(400, json={"invalid": "response"})
    )


@pytest.fixture
def mock_protocol_error(httpx_mock: respx.MockRouter, mock_server: str):
    url = f"{mock_server}/api/amid/action/SomeAction"
    httpx_mock.post(url).mock(
        return_value=httpx.Response(
            200, json=[{"Response": "Error", "Message": "Protocol Error"}]
        )
    )


@pytest.fixture
def mock_invalid_protocol_error(httpx_mock: respx.MockRouter, mock_server: str):
    url = f"{mock_server}/api/amid/action/SomeAction"
    httpx_mock.post(url).mock(
        return_value=httpx.Response(200, json=[{"Invalid": "Error"}])
    )


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
