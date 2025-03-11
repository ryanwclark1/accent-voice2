# Copyright 2025 Accent Communications

from __future__ import annotations

import asyncio
import logging
from functools import lru_cache
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from accent_auth_client.exceptions import (
    InvalidTokenException,
    MissingPermissionsTokenException,
)
from accent_auth_client.type_definitions import JSON, TokenDict

logger = logging.getLogger(__name__)


class TokenCommand(RESTCommand):
    """Command for token-related operations.

    Provides methods for creating, validating, and managing authentication tokens.
    """

    resource = "token"
    _user_agent = "Accent Python auth client"

    async def new_async(
        self,
        backend: str | None = None,
        expiration: int | None = None,
        session_type: str | None = None,
        user_agent: str | None = None,
        access_type: str | None = None,
        client_id: str | None = None,
        refresh_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        tenant_id: str | None = None,
        domain_name: str | None = None,
    ) -> TokenDict:
        """Create a new token asynchronously.

        Args:
            backend: Authentication backend name
            expiration: Token expiration time in seconds
            session_type: Type of session
            user_agent: User agent string
            access_type: Type of access
            client_id: Client identifier
            refresh_token: Refresh token
            username: Username for authentication
            password: Password for authentication
            tenant_id: Tenant identifier
            domain_name: Domain name

        Returns:
            TokenDict: Created token information

        Raises:
            AccentAPIError: If the request fails

        """
        data: dict[str, Any] = {}
        if backend:
            data["backend"] = backend
        if expiration:
            data["expiration"] = expiration
        if client_id:
            data["client_id"] = client_id
        if refresh_token:
            data["refresh_token"] = refresh_token
        if access_type:
            data["access_type"] = access_type
        if tenant_id:
            data["tenant_id"] = tenant_id
        if domain_name:
            data["domain_name"] = domain_name

        headers = self._get_headers()
        headers["User-Agent"] = self._user_agent
        if session_type:
            headers["Accent-Session-Type"] = session_type
        if user_agent:
            headers["User-Agent"] = user_agent

        auth = None
        if username and password:
            auth = httpx.BasicAuth(username=username, password=password)

        client = self.async_client
        if auth:
            client.auth = auth

        start_time = asyncio.get_event_loop().time()

        r = await client.post(self.base_url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(
                "Failed to create token: %s, status code: %s", str(e), r.status_code
            )
            self.raise_from_response(r)

        response = self.process_json_response(r, start_time)
        return cast(TokenDict, response.data["data"])

    def new(
        self,
        backend: str | None = None,
        expiration: int | None = None,
        session_type: str | None = None,
        user_agent: str | None = None,
        access_type: str | None = None,
        client_id: str | None = None,
        refresh_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        tenant_id: str | None = None,
        domain_name: str | None = None,
    ) -> TokenDict:
        """Create a new token.

        Args:
            backend: Authentication backend name
            expiration: Token expiration time in seconds
            session_type: Type of session
            user_agent: User agent string
            access_type: Type of access
            client_id: Client identifier
            refresh_token: Refresh token
            username: Username for authentication
            password: Password for authentication
            tenant_id: Tenant identifier
            domain_name: Domain name

        Returns:
            TokenDict: Created token information

        Raises:
            AccentAPIError: If the request fails

        """
        data: dict[str, Any] = {}
        if backend:
            data["backend"] = backend
        if expiration:
            data["expiration"] = expiration
        if client_id:
            data["client_id"] = client_id
        if refresh_token:
            data["refresh_token"] = refresh_token
        if access_type:
            data["access_type"] = access_type
        if tenant_id:
            data["tenant_id"] = tenant_id
        if domain_name:
            data["domain_name"] = domain_name

        headers = self._get_headers()
        headers["User-Agent"] = self._user_agent
        if session_type:
            headers["Accent-Session-Type"] = session_type
        if user_agent:
            headers["User-Agent"] = user_agent

        auth = None
        if username and password:
            auth = httpx.BasicAuth(username=username, password=password)

        client = self.sync_client
        if auth:
            client.auth = auth

        r = client.post(self.base_url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        response = self.process_json_response(r)
        return cast(TokenDict, response.data["data"])

    async def delete_async(
        self, user_uuid: str, client_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete a token asynchronously.

        Args:
            user_uuid: User identifier
            client_id: Client identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("users", user_uuid, "tokens", client_id)

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error(
                    "Failed to delete token: %s, status code: %s", str(e), r.status_code
                )
                self.raise_from_response(r)

    def delete(
        self, user_uuid: str, client_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete a token.

        Args:
            user_uuid: User identifier
            client_id: Client identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url("users", user_uuid, "tokens", client_id)

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def revoke_async(self, token: str) -> None:
        """Revoke a token asynchronously.

        Args:
            token: Token to revoke

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        await self.async_client.delete(url, headers=headers)

    def revoke(self, token: str) -> None:
        """Revoke a token.

        Args:
            token: Token to revoke

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        self.sync_client.delete(url, headers=headers)

    async def check_async(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        """Check if a token is valid asynchronously.

        Args:
            token: Token to check
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            bool: True if the token is valid

        Raises:
            InvalidTokenException: If the token is invalid
            MissingPermissionsTokenException: If the token lacks permissions
            AccentAPIError: For other API errors

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = await self.async_client.head(url, headers=headers, params=params)

        if r.status_code == 204:
            return True
        if r.status_code == 404:
            raise InvalidTokenException()
        if r.status_code == 403:
            raise MissingPermissionsTokenException()
        self.raise_from_response(r)
        return False

    def check(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        """Check if a token is valid.

        Args:
            token: Token to check
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            bool: True if the token is valid

        Raises:
            InvalidTokenException: If the token is invalid
            MissingPermissionsTokenException: If the token lacks permissions
            AccentAPIError: For other API errors

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = self.sync_client.head(url, headers=headers, params=params)

        if r.status_code == 204:
            return True
        if r.status_code == 404:
            raise InvalidTokenException()
        if r.status_code == 403:
            raise MissingPermissionsTokenException()
        self.raise_from_response(r)
        return False

    @lru_cache(maxsize=128)
    async def is_valid_async(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        """Check if a token is valid without raising exceptions (async).

        Args:
            token: Token to check
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            bool: True if the token is valid

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = await self.async_client.head(url, headers=headers, params=params)

        if r.status_code in (204, 403, 404):
            return r.status_code == 204
        try:
            self.raise_from_response(r)
        except Exception as e:
            logger.exception("Error checking token validity: %s", str(e))
            return False
        return False

    @lru_cache(maxsize=128)
    def is_valid(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        """Check if a token is valid without raising exceptions.

        Args:
            token: Token to check
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            bool: True if the token is valid

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = self.sync_client.head(url, headers=headers, params=params)

        if r.status_code in (204, 403, 404):
            return r.status_code == 204
        try:
            self.raise_from_response(r)
        except Exception as e:
            logger.exception("Error checking token validity: %s", str(e))
            return False
        return False

    async def check_scopes_async(
        self, token: str, scopes: list[str], tenant: str | None = None
    ) -> JSON:
        """Check token scopes asynchronously.

        Args:
            token: Token to check
            scopes: List of scopes to check
            tenant: Optional tenant identifier

        Returns:
            JSON: Response data

        Raises:
            AccentAPIError: If the request fails

        """
        data: dict[str, Any] = {"scopes": scopes}
        if tenant:
            data["tenant_uuid"] = tenant

        headers = self._get_headers()
        headers["User-Agent"] = self._user_agent
        url = f"{self.base_url}/{token}/scopes/check"

        r = await self.async_client.post(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def check_scopes(
        self, token: str, scopes: list[str], tenant: str | None = None
    ) -> JSON:
        """Check token scopes.

        Args:
            token: Token to check
            scopes: List of scopes to check
            tenant: Optional tenant identifier

        Returns:
            JSON: Response data

        Raises:
            AccentAPIError: If the request fails

        """
        data: dict[str, Any] = {"scopes": scopes}
        if tenant:
            data["tenant_uuid"] = tenant

        headers = self._get_headers()
        headers["User-Agent"] = self._user_agent
        url = f"{self.base_url}/{token}/scopes/check"

        r = self.sync_client.post(url, headers=headers, json=data)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_async(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> TokenDict:
        """Get token information asynchronously.

        Args:
            token: Token to get
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            TokenDict: Token information

        Raises:
            AccentAPIError: If the request fails

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = await self.async_client.get(url, headers=headers, params=params)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(TokenDict, r.json()["data"])

    def get(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> TokenDict:
        """Get token information.

        Args:
            token: Token to check
            required_acl: Optional required ACL
            tenant: Optional tenant identifier

        Returns:
            TokenDict: Token information

        Raises:
            AccentAPIError: If the request fails

        """
        params = {}
        if required_acl:
            params["scope"] = required_acl
        if tenant:
            params["tenant"] = tenant

        headers = self._get_headers()
        url = f"{self.base_url}/{token}"

        r = self.sync_client.get(url, headers=headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(TokenDict, r.json()["data"])

    async def list_async(
        self, user_uuid: str | None = None, **kwargs: Any
    ) -> list[TokenDict]:
        """List tokens for a user asynchronously.

        Args:
            user_uuid: User identifier (required)
            **kwargs: Additional parameters

        Returns:
            list[TokenDict]: List of tokens

        Raises:
            TypeError: If user_uuid is None
            AccentAPIError: If the request fails

        """
        if user_uuid is None:
            raise TypeError("user_uuid cannot be None")

        headers = self._get_headers(**kwargs)
        url = self._client.url("users", user_uuid, "tokens")

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(list[TokenDict], r.json())

    def list(self, user_uuid: str | None = None, **kwargs: Any) -> list[TokenDict]:
        """List tokens for a user.

        Args:
            user_uuid: User identifier (required)
            **kwargs: Additional parameters

        Returns:
            list[TokenDict]: List of tokens

        Raises:
            TypeError: If user_uuid is None
            AccentAPIError: If the request fails

        """
        if user_uuid is None:
            raise TypeError("user_uuid cannot be None")

        headers = self._get_headers(**kwargs)
        url = self._client.url("users", user_uuid, "tokens")

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(list[TokenDict], r.json())
