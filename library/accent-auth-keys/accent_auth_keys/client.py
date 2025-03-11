# Copyright 2025 Accent Communications

"""Async HTTP client for communicating with the Accent Auth API."""

import builtins
import logging
from functools import lru_cache
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from .models import ItemsResponse, Policy, TokenResponse, User

# Setup logging
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncClient:
    """Async HTTP client for the Accent Auth API.

    This client replaces the accent_auth_client.Client from the original codebase,
    providing async capabilities with httpx.

    Args:
        base_url: Base URL for the API.
        **kwargs: Additional arguments to pass to httpx.AsyncClient.

    """

    def __init__(self, base_url: str, **kwargs: Any) -> None:
        """Initialize the AsyncClient.

        Args:
            base_url: The base URL for API requests.
            **kwargs: Additional keyword arguments for httpx.AsyncClient.

        """
        self.base_url = base_url.rstrip("/")
        self.client_kwargs = kwargs
        self._token: str | None = None
        self.users = UsersAPI(self)
        self.policies = PoliciesAPI(self)
        self.token = TokenAPI(self)

    async def _get_client(self) -> httpx.AsyncClient:
        """Get an httpx AsyncClient with the proper configuration.

        Returns:
            An httpx.AsyncClient instance.

        """
        headers = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        return httpx.AsyncClient(
            base_url=self.base_url, headers=headers, **self.client_kwargs
        )

    def set_token(self, token: str) -> None:
        """Set the authentication token.

        Args:
            token: The authentication token.

        """
        self._token = token

    @lru_cache(maxsize=32)
    async def _request(
        self, method: str, path: str, model: type[T] | None = None, **kwargs: Any
    ) -> T | dict[str, Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            model: Optional Pydantic model to parse the response into.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            API response, either as a Pydantic model or a dictionary.

        """
        async with await self._get_client() as client:
            url = f"{self.base_url}/{path.lstrip('/')}"
            logger.debug(f"Requesting {method} {url}")

            response = await client.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Response: {data}")

            if model:
                return model.model_validate(data)
            return data


class UsersAPI:
    """API endpoints for user management."""

    def __init__(self, client: AsyncClient) -> None:
        """Initialize the UsersAPI.

        Args:
            client: The AsyncClient instance.

        """
        self.client = client

    async def list(self, **params: Any) -> ItemsResponse:
        """List users.

        Args:
            **params: Query parameters for filtering users.

        Returns:
            Response containing a list of users.

        """
        return await self.client._request("GET", "users", ItemsResponse, params=params)

    async def new(self, username: str, password: str, purpose: str) -> User:
        """Create a new user.

        Args:
            username: Username for the new user.
            password: Password for the new user.
            purpose: Purpose of the user.

        Returns:
            The created user.

        """
        data = {"username": username, "password": password, "purpose": purpose}
        return await self.client._request("POST", "users", User, json=data)

    async def delete(self, user_uuid: str) -> None:
        """Delete a user.

        Args:
            user_uuid: UUID of the user to delete.

        """
        await self.client._request("DELETE", f"users/{user_uuid}")

    async def get_policies(self, user_uuid: str) -> ItemsResponse:
        """Get policies for a user.

        Args:
            user_uuid: UUID of the user.

        Returns:
            Response containing a list of policies.

        """
        return await self.client._request(
            "GET", f"users/{user_uuid}/policies", ItemsResponse
        )

    async def add_policy(self, user_uuid: str, policy_uuid: str) -> dict[str, Any]:
        """Add a policy to a user.

        Args:
            user_uuid: UUID of the user.
            policy_uuid: UUID of the policy to add.

        Returns:
            API response.

        """
        data = {"policy_uuid": policy_uuid}
        return await self.client._request(
            "POST", f"users/{user_uuid}/policies", json=data
        )


class PoliciesAPI:
    """API endpoints for policy management."""

    def __init__(self, client: AsyncClient) -> None:
        """Initialize the PoliciesAPI.

        Args:
            client: The AsyncClient instance.

        """
        self.client = client

    async def list(self, **params: Any) -> ItemsResponse:
        """List policies.

        Args:
            **params: Query parameters for filtering policies.

        Returns:
            Response containing a list of policies.

        """
        return await self.client._request(
            "GET", "policies", ItemsResponse, params=params
        )

    async def new(self, name: str, acl: builtins.list[str]) -> Policy:
        """Create a new policy.

        Args:
            name: Name of the policy.
            acl: Access control list for the policy.

        Returns:
            The created policy.

        """
        data = {"name": name, "acl": acl}
        return await self.client._request("POST", "policies", Policy, json=data)

    async def edit(self, policy_uuid: str, name: str, acl: builtins.list[str]) -> Policy:
        """Edit a policy.

        Args:
            policy_uuid: UUID of the policy to edit.
            name: New name of the policy.
            acl: New access control list for the policy.

        Returns:
            The updated policy.

        """
        data = {"name": name, "acl": acl}
        return await self.client._request(
            "PUT", f"policies/{policy_uuid}", Policy, json=data
        )

    async def delete(self, policy_uuid: str) -> None:
        """Delete a policy.

        Args:
            policy_uuid: UUID of the policy to delete.

        """
        await self.client._request("DELETE", f"policies/{policy_uuid}")


class TokenAPI:
    """API endpoints for token management."""

    def __init__(self, client: AsyncClient) -> None:
        """Initialize the TokenAPI.

        Args:
            client: The AsyncClient instance.

        """
        self.client = client

    async def new(self, grant_type: str, expiration: int = 600) -> TokenResponse:
        """Get a new token.

        Args:
            grant_type: Type of grant for the token.
            expiration: Expiration time in seconds.

        Returns:
            Response containing the token.

        """
        data = {"grant_type": grant_type, "expiration": expiration}
        return await self.client._request("POST", "token", TokenResponse, json=data)
