# tests/conftest.py
import asyncio
import json
import threading
from typing import Any, AsyncGenerator, Generator

import httpx
import pytest
import respx
from accent_lib_rest_client.client import BaseClient
from accent_lib_rest_client.config import Config

from accent_agentd_client import Client
from accent_agentd_client.error import (
    ALREADY_IN_QUEUE,
    ALREADY_IN_USE,
    ALREADY_LOGGED,
    CONTEXT_DIFFERENT_TENANT,
    NOT_IN_QUEUE,
    NOT_LOGGED,
    NO_SUCH_AGENT,
    NO_SUCH_EXTEN,
    NO_SUCH_LINE,
    NO_SUCH_QUEUE,
    QUEUE_DIFFERENT_TENANT,
    UNAUTHORIZED,
)

# Constants for mock server
MOCK_SERVER_HOST = "127.0.0.1"
MOCK_SERVER_PORT = 8000
BASE_URL = f"http://{MOCK_SERVER_HOST}:{MOCK_SERVER_PORT}/api/agentd/1.0"
AGENT_ID = "123"
AGENT_NUMBER = "456"
EXTENSION = "789"
CONTEXT = "default"
LINE_ID = "321"
QUEUE_ID = "987"
TENANT_UUID = "654321"
INVALID_TENANT_UUID = "99999999-9999-9999-9999-999999999999"


# --- Mock Responses ---
@pytest.fixture
def mock_agent_status_logged_in() -> dict[str, Any]:
    return {
        "id": AGENT_ID,
        "number": AGENT_NUMBER,
        "origin_uuid": "some_uuid",
        "logged": True,
        "paused": False,
        "extension": EXTENSION,
        "context": CONTEXT,
        "state_interface": "SIP/123",
        "tenant_uuid": TENANT_UUID,
    }


@pytest.fixture
def mock_agent_status_logged_out() -> dict[str, Any]:
    return {
        "id": "124",
        "number": "457",
        "origin_uuid": "another_uuid",
        "logged": False,  # Logged out
        "paused": True,
        "extension": "790",
        "context": "another_context",
        "state_interface": "SIP/124",
        "tenant_uuid": TENANT_UUID,
    }


@pytest.fixture
def mock_agent_statuses_multiple(
    mock_agent_status_logged_in, mock_agent_status_logged_out
) -> list[dict[str, Any]]:
    return [mock_agent_status_logged_in, mock_agent_status_logged_out]


@pytest.fixture
def mock_agent_statuses_empty() -> list[dict[str, Any]]:
    return []  # Empty list


@pytest.fixture
def mock_service_status() -> dict[str, Any]:
    return {"status": "OK", "version": "1.0"}


@pytest.fixture
def mock_no_such_agent_error() -> dict[str, Any]:
    return {"error": NO_SUCH_AGENT}


@pytest.fixture
def mock_unauthorized_error() -> dict[str, Any]:
    return {"error": UNAUTHORIZED}


@pytest.fixture(scope="session")
def mock_server() -> Generator[None, None, None]:
    """Starts the mock FastAPI server in a separate thread."""
    from .mocks.server import app
    import uvicorn

    # Use a threading lock to prevent the server from starting multiple times
    # if the tests are run with xdist.
    lock = threading.Lock()
    with lock:
        thread = None
        if not any(
            "mock_server" in t.name for t in threading.enumerate()
        ):  # added to handle multiple test runs.
            thread = threading.Thread(
                target=uvicorn.run,
                kwargs={
                    "app": app,
                    "host": MOCK_SERVER_HOST,
                    "port": MOCK_SERVER_PORT,
                    "log_level": "critical",
                },
                name="mock_server_thread",  # Named the thread
                daemon=True,
            )
            thread.start()

    yield

    if thread:
        thread.join(timeout=0.1)  # Ensure thread is joined


@pytest.fixture(scope="session")
def test_config() -> Config:
    """Creates a configuration for testing."""
    return Config(host=MOCK_SERVER_HOST, port=MOCK_SERVER_PORT)


@pytest.fixture
def mock_client(test_config: Config) -> Client:
    """Creates a test client instance connected to the mock server."""
    return Client(host=test_config.host, port=test_config.port, token=test_config.token)


@pytest.fixture
def base_mock_client(test_config: Config) -> BaseClient:
    """Creates a test client instance connected to the mock server."""
    return BaseClient(
        host=test_config.host, port=test_config.port, token=test_config.token
    )


@pytest.fixture
def respx_mock() -> respx.MockRouter:
    """Provides a respx mock router for mocking httpx requests."""
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as respx_mock:
        yield respx_mock


@pytest.fixture  # Keep logic, add varied responses.
def httpx_mock(
    respx_mock: respx.MockRouter,
    mock_agent_status_logged_in,
    mock_agent_status_logged_out,
    mock_agent_statuses_multiple,
    mock_agent_statuses_empty,
    mock_service_status,
    mock_no_such_agent_error,
    mock_unauthorized_error,
) -> respx.MockRouter:
    """Defines common mock API responses using respx."""

    # Mock agent status responses (using the new fixtures)
    respx_mock.get(f"/by-id/{AGENT_ID}").respond(200, json=mock_agent_status_logged_in)
    respx_mock.get(f"/by-number/{AGENT_NUMBER}").respond(
        200, json=mock_agent_status_logged_in
    )
    respx_mock.get("/users/me/agents").respond(200, json=mock_agent_status_logged_in)

    # Mock multiple statuses (including empty list)
    respx_mock.get("").with_params(recurse="true").respond(
        200, json=mock_agent_statuses_multiple
    )
    respx_mock.get("").with_params(recurse="false").respond(
        200, json=mock_agent_statuses_empty
    )
    respx_mock.get("").respond(
        200, json=mock_agent_statuses_empty
    )  # Default (no params)

    # Mock generic success responses
    respx_mock.post(f"/by-id/{AGENT_ID}/add").respond(204)
    respx_mock.post(f"/by-id/{AGENT_ID}/remove").respond(204)
    respx_mock.post(f"/by-id/{AGENT_ID}/login").respond(204)
    respx_mock.post(f"/by-number/{AGENT_NUMBER}/login").respond(204)
    respx_mock.post(f"/by-id/{AGENT_ID}/logoff").respond(204)
    respx_mock.post(f"/by-number/{AGENT_NUMBER}/logoff").respond(204)
    respx_mock.post(f"/by-number/{AGENT_NUMBER}/pause").respond(204)
    respx_mock.post(f"/by-number/{AGENT_NUMBER}/unpause").respond(204)
    respx_mock.post("/logoff").respond(204)
    respx_mock.post("/relog").respond(204)
    respx_mock.post("/users/me/agents/login").respond(204)
    respx_mock.post("/users/me/agents/logoff").respond(204)
    respx_mock.post("/users/me/agents/pause").respond(204)
    respx_mock.post("/users/me/agents/unpause").respond(204)

    # Mock service status
    respx_mock.get("/status").respond(200, json=mock_service_status)

    # --- Mock Error Responses (using fixtures) ---
    respx_mock.get(f"/by-id/invalid_agent").respond(404, json=mock_no_such_agent_error)
    # ... Add more specific routes for other errors if needed ...
    # Generic error handler (for any other 4xx/5xx errors)
    respx_mock.route(status_code__gte=400).pass_through().mock(
        return_value=httpx.Response(500, json={"error": "Unhandled Error"})
    )

    return respx_mock


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, Any]:
    """
    Provides the event loop for pytest-asyncio.

    This fixture is necessary because of a bug in pytest-asyncio.
    See https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264418154
    for more details.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
