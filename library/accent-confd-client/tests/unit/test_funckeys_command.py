# Copyright 2025 Accent Communications

"""Tests for the FuncKeys command."""

from typing import Any, Dict

import httpx
import pytest
from accent_confd_client.client import ConfdClient
from pytest_httpx import HTTPXMock

from tests.mocks.responses import sample_funckeys


def test_list_templates(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test listing function key templates.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/funckeys/templates",
        json={
            "items": [{"id": 1, "name": "Template 1"}, {"id": 2, "name": "Template 2"}],
            "total": 2,
        },
    )

    # Call the API
    result = client.funckeys.list()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == 1
    assert result["items"][1]["id"] == 2


@pytest.mark.asyncio
async def test_list_templates_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test listing function key templates asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/funckeys/templates",
        json={
            "items": [{"id": 1, "name": "Template 1"}, {"id": 2, "name": "Template 2"}],
            "total": 2,
        },
    )

    # Call the API asynchronously
    result = await client.funckeys.list_async()

    # Verify the result
    assert "items" in result
    assert len(result["items"]) == 2
    assert result["items"][0]["id"] == 1
    assert result["items"][1]["id"] == 2


def test_get_template(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting a function key template.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/funckeys/templates/1",
        json={"id": 1, "name": "Template 1", "keys": sample_funckeys["keys"]},
    )

    # Call the API
    result = client.funckeys.get(1)

    # Verify the result
    assert result["id"] == 1
    assert result["name"] == "Template 1"
    assert "keys" in result
    assert "1" in result["keys"]
    assert "2" in result["keys"]


def test_get_template_funckey(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting a specific function key from a template.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/funckeys/templates/1/1",
        json=sample_funckeys["keys"]["1"],
    )

    # Call the API
    result = client.funckeys.get_template_funckey(1, "1")

    # Verify the result
    assert result["type"] == "speeddial"
    assert result["label"] == "Speed Dial 1"
    assert result["destination"]["type"] == "user"
    assert result["destination"]["user_id"] == 1


@pytest.mark.asyncio
async def test_get_template_funckey_async(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test getting a specific function key from a template asynchronously.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/funckeys/templates/1/1",
        json=sample_funckeys["keys"]["1"],
    )

    # Call the API asynchronously
    result = await client.funckeys.get_template_funckey_async(1, "1")

    # Verify the result
    assert result["type"] == "speeddial"
    assert result["label"] == "Speed Dial 1"
    assert result["destination"]["type"] == "user"


def test_update_template_funckey(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test updating a function key in a template.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Define function key data
    funckey = {
        "type": "speeddial",
        "label": "Updated Speed Dial",
        "destination": {"type": "user", "user_id": 3},
    }

    # Configure mock response
    httpx_mock.add_response(
        method="PUT", url=f"{base_url}/funckeys/templates/1/1", status_code=204
    )

    # Call the API
    client.funckeys.update_template_funckey(1, "1", funckey)

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "PUT"
    assert request.url == f"{base_url}/funckeys/templates/1/1"
    assert request.json() == funckey


def test_delete_template_funckey(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test deleting a function key from a template.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock response
    httpx_mock.add_response(
        method="DELETE", url=f"{base_url}/funckeys/templates/1/1", status_code=204
    )

    # Call the API
    client.funckeys.delete_template_funckey(1, "1")

    # Verify the request
    request = httpx_mock.get_request()
    assert request.method == "DELETE"
    assert request.url == f"{base_url}/funckeys/templates/1/1"


def test_template_relation(
    client: ConfdClient, httpx_mock: HTTPXMock, base_url: str
) -> None:
    """Test template relations.

    Args:
        client: Client instance
        httpx_mock: HTTP mock fixture
        base_url: Base URL for API requests

    """
    # Configure mock responses for user operations
    httpx_mock.add_response(
        method="PUT",
        url=f"{base_url}/users/user1-uuid/funckeys/templates/1",
        status_code=204,
    )

    httpx_mock.add_response(
        method="DELETE",
        url=f"{base_url}/users/user1-uuid/funckeys/templates/1",
        status_code=204,
    )

    # Test getting template relation
    template_relation = client.funckeys.relations(1)
    assert template_relation is not None

    # Test adding a user
    template_relation.add_user("user1-uuid")
    request = httpx_mock.get_request(0)
    assert request.method == "PUT"
    assert request.url == f"{base_url}/users/user1-uuid/funckeys/templates/1"

    # Test removing a user
    template_relation.remove_user("user1-uuid")
    request = httpx_mock.get_request(1)
    assert request.method == "DELETE"
    assert request.url == f"{base_url}/users/user1-uuid/funckeys/templates/1"
