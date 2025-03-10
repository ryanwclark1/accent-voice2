# Copyright 2025 Accent Communications

from __future__ import annotations

import builtins
import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)

class UsersCommand(RESTCommand):
    """Command for user-related operations.

    Provides methods for managing users and their relationships.
    """

    resource = "users"
    _ro_headers = {"Accept": "application/json"}
    _rw_headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async def add_policy_async(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Add a policy to a user asynchronously.

        Args:
            user_uuid: User identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/policies/{policy_uuid}"

        r = await self.async_client.put(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to add policy: %s, status code: %s",
                            str(e), r.status_code)
                self.raise_from_response(r)

    def add_policy(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Add a policy to a user.

        Args:
            user_uuid: User identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/policies/{policy_uuid}"

        r = self.sync_client.put(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def change_password_async(self, user_uuid: str, **kwargs: Any) -> None:
        """Change a user's password asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: Password-related parameters

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, user_uuid, "password"])

        r = await self.async_client.put(url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to change password: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def change_password(self, user_uuid: str, **kwargs: Any) -> None:
        """Change a user's password.

        Args:
            user_uuid: User identifier
            **kwargs: Password-related parameters

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = "/".join([self.base_url, user_uuid, "password"])

        r = self.sync_client.put(url, headers=headers, json=kwargs)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def delete_async(self, user_uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a user asynchronously.

        Args:
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to delete user: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def delete(self, user_uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a user.

        Args:
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def edit_async(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Edit a user asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: User properties to update

        Returns:
            JSON: Updated user information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)
        url = f"{self.base_url}/{user_uuid}"

        r = await self.async_client.put(url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def edit(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Edit a user.

        Args:
            user_uuid: User identifier
            **kwargs: User properties to update

        Returns:
            JSON: Updated user information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)
        url = f"{self.base_url}/{user_uuid}"

        r = self.sync_client.put(url, headers=headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_async(self, user_uuid: str, tenant_uuid: str | None = None) -> JSON:
        """Get user information asynchronously.

        Args:
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: User information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def get(self, user_uuid: str, tenant_uuid: str | None = None) -> JSON:
        """Get user information.

        Args:
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier

        Returns:
            JSON: User information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def get_groups_async(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user groups asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User groups

        Raises:
            AccentAPIError: If the request fails

        """
        return await self._get_relation_async("groups", user_uuid, **kwargs)

    def get_groups(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user groups.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User groups

        Raises:
            AccentAPIError: If the request fails

        """
        return self._get_relation("groups", user_uuid, **kwargs)

    async def get_policies_async(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user policies asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User policies

        Raises:
            AccentAPIError: If the request fails

        """
        return await self._get_relation_async("policies", user_uuid, **kwargs)

    def get_policies(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user policies.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User policies

        Raises:
            AccentAPIError: If the request fails

        """
        return self._get_relation("policies", user_uuid, **kwargs)

    async def get_sessions_async(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user sessions asynchronously.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User sessions

        Raises:
            AccentAPIError: If the request fails

        """
        return await self._get_relation_async("sessions", user_uuid, **kwargs)

    def get_sessions(self, user_uuid: str, **kwargs: Any) -> JSON:
        """Get user sessions.

        Args:
            user_uuid: User identifier
            **kwargs: Additional parameters

        Returns:
            JSON: User sessions

        Raises:
            AccentAPIError: If the request fails

        """
        return self._get_relation("sessions", user_uuid, **kwargs)

    async def list_async(self, **kwargs: Any) -> JSON:
        """List users asynchronously.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, **kwargs: Any) -> JSON:
        """List users.

        Args:
            **kwargs: Filter parameters

        Returns:
            JSON: List of users

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def new_async(self, **kwargs: Any) -> JSON:
        """Create a new user asynchronously.

        Args:
            **kwargs: User properties

        Returns:
            JSON: Created user information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.post(self.base_url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def new(self, **kwargs: Any) -> JSON:
        """Create a new user.

        Args:
            **kwargs: User properties

        Returns:
            JSON: Created user information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def register_async(self, **kwargs: Any) -> JSON:
        """Register a new user asynchronously.

        Args:
            **kwargs: Registration properties

        Returns:
            JSON: Registration response

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/register"

        r = await self.async_client.post(url, headers=headers, json=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def register(self, **kwargs: Any) -> JSON:
        """Register a new user.

        Args:
            **kwargs: Registration properties

        Returns:
            JSON: Registration response

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/register"

        r = self.sync_client.post(url, headers=headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def remove_policy_async(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove a policy from a user asynchronously.

        Args:
            user_uuid: User identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/policies/{policy_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to remove policy: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def remove_policy(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Remove a policy from a user.

        Args:
            user_uuid: User identifier
            policy_uuid: Policy identifier
            tenant_uuid: Optional tenant identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/policies/{policy_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def remove_session_async(self, user_uuid: str, session_uuid: str) -> None:
        """Remove a session for a user asynchronously.

        Args:
            user_uuid: User identifier
            session_uuid: Session identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/sessions/{session_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to remove session: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def remove_session(self, user_uuid: str, session_uuid: str) -> None:
        """Remove a session for a user.

        Args:
            user_uuid: User identifier
            session_uuid: Session identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/sessions/{session_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def request_confirmation_email_async(self, user_uuid: str, email_uuid: str) -> None:
        """Request a confirmation email asynchronously.

        Args:
            user_uuid: User identifier
            email_uuid: Email identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/emails/{email_uuid}/confirm"

        r = await self.async_client.get(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to request confirmation email: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def request_confirmation_email(self, user_uuid: str, email_uuid: str) -> None:
        """Request a confirmation email.

        Args:
            user_uuid: User identifier
            email_uuid: Email identifier

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/emails/{email_uuid}/confirm"

        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def reset_password_async(self, **kwargs: Any) -> None:
        """Reset a user's password asynchronously.

        Args:
            **kwargs: Password reset parameters

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/password/reset"

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to reset password: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def reset_password(self, **kwargs: Any) -> None:
        """Reset a user's password.

        Args:
            **kwargs: Password reset parameters

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/password/reset"

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def set_password_async(
        self, user_uuid: str, password: str, token: str | None = None
    ) -> None:
        """Set a user's password asynchronously.

        Args:
            user_uuid: User identifier
            password: New password
            token: Optional authentication token

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/password/reset"
        query_string = {"user_uuid": user_uuid}
        body = {"password": password}
        headers = self._get_headers()
        if token:
            headers["X-Auth-Token"] = token

        r = await self.async_client.post(
            url, headers=headers, params=query_string, json=body
        )

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to set password: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def set_password(
        self, user_uuid: str, password: str, token: str | None = None
    ) -> None:
        """Set a user's password.

        Args:
            user_uuid: User identifier
            password: New password
            token: Optional authentication token

        Raises:
            AccentAPIError: If the request fails

        """
        url = f"{self.base_url}/password/reset"
        query_string = {"user_uuid": user_uuid}
        body = {"password": password}
        headers = self._get_headers()
        if token:
            headers["X-Auth-Token"] = token

        r = self.sync_client.post(
            url, headers=headers, params=query_string, json=body
        )

        if r.status_code != 204:
            self.raise_from_response(r)

    async def update_emails_async(self, user_uuid: str, emails: builtins.list[str]) -> JSON:
        """Update user emails asynchronously.

        Args:
            user_uuid: User identifier
            emails: List of email addresses

        Returns:
            JSON: Updated email information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/emails"
        body = {"emails": emails}

        r = await self.async_client.put(url, headers=headers, json=body)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def update_emails(self, user_uuid: str, emails: builtins.list[str]) -> JSON:
        """Update user emails.

        Args:
            user_uuid: User identifier
            emails: List of email addresses

        Returns:
            JSON: Updated email information

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers()
        url = f"{self.base_url}/{user_uuid}/emails"
        body = {"emails": emails}

        r = self.sync_client.put(url, headers=headers, json=body)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def _get_relation_async(
        self,
        resource: str,
        user_uuid: str,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSON:
        """Get a user relation asynchronously.

        Args:
            resource: Relation resource name
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional parameters

        Returns:
            JSON: Relation data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/{resource}"

        r = await self.async_client.get(url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def _get_relation(
        self,
        resource: str,
        user_uuid: str,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> JSON:
        """Get a user relation.

        Args:
            resource: Relation resource name
            user_uuid: User identifier
            tenant_uuid: Optional tenant identifier
            **kwargs: Additional parameters

        Returns:
            JSON: Relation data

        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{user_uuid}/{resource}"

        r = self.sync_client.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return cast(JSON, r.json())
