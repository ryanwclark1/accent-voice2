# Copyright 2025 Accent Communications

"""Commands for managing Webhookd subscriptions.

This module provides commands for creating, listing, updating, and
deleting subscriptions in the Webhookd service.
"""

from __future__ import annotations

import builtins
import logging
from typing import Any
from uuid import UUID

from accent_webhookd_client.command import WebhookdCommand
from accent_webhookd_client.models import (
    ServicesDict,
    SubscriptionListResponse,
    SubscriptionLogListResponse,
    SubscriptionModel,
    UserSubscriptionListResponse,
    UserSubscriptionModel,
)

# Configure logging
logger = logging.getLogger(__name__)


class SubscriptionsCommand(WebhookdCommand):
    """Command for managing Webhookd subscriptions.

    This command allows creating, listing, updating, and deleting
    subscriptions in the Webhookd service.
    """

    resource = "subscriptions"

    def _metadata_params(self, search_metadata: dict[str, str]) -> builtins.list[str]:
        """Convert metadata dictionary to query parameter format.

        Args:
            search_metadata: Metadata key-value pairs to search for

        Returns:
            List of formatted metadata parameters

        """
        return [f"{key}:{value}" for key, value in search_metadata.items()]

    def create(
        self, subscription: SubscriptionModel | dict[str, Any]
    ) -> SubscriptionModel:
        """Create a new subscription.

        Args:
            subscription: Subscription data

        Returns:
            Created subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Creating new subscription")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, SubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = self._sync_request(
            "post", self.base_url, headers=headers, json=subscription
        )
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    async def create_async(
        self, subscription: SubscriptionModel | dict[str, Any]
    ) -> SubscriptionModel:
        """Create a new subscription asynchronously.

        Args:
            subscription: Subscription data

        Returns:
            Created subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Creating new subscription (async)")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, SubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = await self._async_request(
            "post", self.base_url, headers=headers, json=subscription
        )
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    def create_as_user(
        self, subscription: UserSubscriptionModel | dict[str, Any]
    ) -> UserSubscriptionModel:
        """Create a new user subscription.

        Args:
            subscription: User subscription data

        Returns:
            Created user subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Creating new user subscription")
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, UserSubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = self._sync_request("post", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    async def create_as_user_async(
        self, subscription: UserSubscriptionModel | dict[str, Any]
    ) -> UserSubscriptionModel:
        """Create a new user subscription asynchronously.

        Args:
            subscription: User subscription data

        Returns:
            Created user subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Creating new user subscription (async)")
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, UserSubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = await self._async_request("post", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    def list(
        self, search_metadata: dict[str, str] | None = None, recurse: bool = False
    ) -> SubscriptionListResponse:
        """List subscriptions, optionally filtered by metadata.

        Args:
            search_metadata: Optional metadata to filter by
            recurse: Whether to include child subscriptions

        Returns:
            List of matching subscriptions

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing subscriptions")
        params: dict[str, Any] = {}
        if search_metadata:
            params["search_metadata"] = self._metadata_params(search_metadata)
        if recurse:
            params["recurse"] = True

        headers = self._get_headers()
        r = self._sync_request("get", self.base_url, params=params, headers=headers)
        self.raise_from_response(r)
        return SubscriptionListResponse.model_validate(r.json())

    async def list_async(
        self, search_metadata: dict[str, str] | None = None, recurse: bool = False
    ) -> SubscriptionListResponse:
        """List subscriptions asynchronously, optionally filtered by metadata.

        Args:
            search_metadata: Optional metadata to filter by
            recurse: Whether to include child subscriptions

        Returns:
            List of matching subscriptions

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing subscriptions (async)")
        params: dict[str, Any] = {}
        if search_metadata:
            params["search_metadata"] = self._metadata_params(search_metadata)
        if recurse:
            params["recurse"] = True

        headers = self._get_headers()
        r = await self._async_request(
            "get", self.base_url, params=params, headers=headers
        )
        self.raise_from_response(r)
        return SubscriptionListResponse.model_validate(r.json())

    def list_as_user(
        self, search_metadata: dict[str, str] | None = None
    ) -> UserSubscriptionListResponse:
        """List user subscriptions, optionally filtered by metadata.

        Args:
            search_metadata: Optional metadata to filter by

        Returns:
            List of matching user subscriptions

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing user subscriptions")
        params = {}
        if search_metadata:
            params["search_metadata"] = self._metadata_params(search_metadata)

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self._sync_request("get", url, params=params, headers=headers)
        self.raise_from_response(r)
        return UserSubscriptionListResponse.model_validate(r.json())

    async def list_as_user_async(
        self, search_metadata: dict[str, str] | None = None
    ) -> UserSubscriptionListResponse:
        """List user subscriptions asynchronously, optionally filtered by metadata.

        Args:
            search_metadata: Optional metadata to filter by

        Returns:
            List of matching user subscriptions

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing user subscriptions (async)")
        params = {}
        if search_metadata:
            params["search_metadata"] = self._metadata_params(search_metadata)

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self._async_request("get", url, params=params, headers=headers)
        self.raise_from_response(r)
        return UserSubscriptionListResponse.model_validate(r.json())

    def get(self, subscription_uuid: str | UUID) -> SubscriptionModel:
        """Get a subscription by UUID.

        Args:
            subscription_uuid: UUID of the subscription

        Returns:
            Subscription details

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))
        r = self._sync_request("get", url, headers=headers)
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    async def get_async(self, subscription_uuid: str | UUID) -> SubscriptionModel:
        """Get a subscription by UUID asynchronously.

        Args:
            subscription_uuid: UUID of the subscription

        Returns:
            Subscription details

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))
        r = await self._async_request("get", url, headers=headers)
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    def get_as_user(self, subscription_uuid: str | UUID) -> UserSubscriptionModel:
        """Get a user subscription by UUID.

        Args:
            subscription_uuid: UUID of the subscription

        Returns:
            User subscription details

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting user subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))
        r = self._sync_request("get", url, headers=headers)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    async def get_as_user_async(
        self, subscription_uuid: str | UUID
    ) -> UserSubscriptionModel:
        """Get a user subscription by UUID asynchronously.

        Args:
            subscription_uuid: UUID of the subscription

        Returns:
            User subscription details

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting user subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))
        r = await self._async_request("get", url, headers=headers)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    def update(
        self,
        subscription_uuid: str | UUID,
        subscription: SubscriptionModel | dict[str, Any],
    ) -> SubscriptionModel:
        """Update a subscription.

        Args:
            subscription_uuid: UUID of the subscription to update
            subscription: Updated subscription data

        Returns:
            Updated subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Updating subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, SubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = self._sync_request("put", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    async def update_async(
        self,
        subscription_uuid: str | UUID,
        subscription: SubscriptionModel | dict[str, Any],
    ) -> SubscriptionModel:
        """Update a subscription asynchronously.

        Args:
            subscription_uuid: UUID of the subscription to update
            subscription: Updated subscription data

        Returns:
            Updated subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Updating subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, SubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = await self._async_request("put", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return SubscriptionModel.model_validate(r.json())

    def update_as_user(
        self,
        subscription_uuid: str | UUID,
        subscription: UserSubscriptionModel | dict[str, Any],
    ) -> UserSubscriptionModel:
        """Update a user subscription.

        Args:
            subscription_uuid: UUID of the subscription to update
            subscription: Updated subscription data

        Returns:
            Updated user subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Updating user subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, UserSubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = self._sync_request("put", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    async def update_as_user_async(
        self,
        subscription_uuid: str | UUID,
        subscription: UserSubscriptionModel | dict[str, Any],
    ) -> UserSubscriptionModel:
        """Update a user subscription asynchronously.

        Args:
            subscription_uuid: UUID of the subscription to update
            subscription: Updated subscription data

        Returns:
            Updated user subscription

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Updating user subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))

        # Convert Pydantic model to dict if needed
        if isinstance(subscription, UserSubscriptionModel):
            subscription = subscription.model_dump(exclude_unset=True)

        r = await self._async_request("put", url, headers=headers, json=subscription)
        self.raise_from_response(r)
        return UserSubscriptionModel.model_validate(r.json())

    def delete(self, subscription_uuid: str | UUID) -> None:
        """Delete a subscription.

        Args:
            subscription_uuid: UUID of the subscription to delete

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Deleting subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))
        r = self._sync_request("delete", url, headers=headers)
        self.raise_from_response(r)
        logger.debug("Subscription deleted successfully")

    async def delete_async(self, subscription_uuid: str | UUID) -> None:
        """Delete a subscription asynchronously.

        Args:
            subscription_uuid: UUID of the subscription to delete

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Deleting subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("subscriptions", str(subscription_uuid))
        r = await self._async_request("delete", url, headers=headers)
        self.raise_from_response(r)
        logger.debug("Subscription deleted successfully")

    def delete_as_user(self, subscription_uuid: str | UUID) -> None:
        """Delete a user subscription.

        Args:
            subscription_uuid: UUID of the subscription to delete

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Deleting user subscription %s", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))
        r = self._sync_request("delete", url, headers=headers)
        self.raise_from_response(r)
        logger.debug("User subscription deleted successfully")

    async def delete_as_user_async(self, subscription_uuid: str | UUID) -> None:
        """Delete a user subscription asynchronously.

        Args:
            subscription_uuid: UUID of the subscription to delete

        Raises:
            WebhookdError: If the request fails

        """
        logger.info("Deleting user subscription %s (async)", subscription_uuid)
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, str(subscription_uuid))
        r = await self._async_request("delete", url, headers=headers)
        self.raise_from_response(r)
        logger.debug("User subscription deleted successfully")

    def list_services(self) -> ServicesDict:
        """List available services.

        Returns:
            Dictionary of available services

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing available services")
        headers = self._get_headers()
        url = self._client.url("subscriptions", "services")
        r = self._sync_request("get", url, headers=headers)
        self.raise_from_response(r)
        return ServicesDict.model_validate(r.json())

    async def list_services_async(self) -> ServicesDict:
        """List available services asynchronously.

        Returns:
            Dictionary of available services

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Listing available services (async)")
        headers = self._get_headers()
        url = self._client.url("subscriptions", "services")
        r = await self._async_request("get", url, headers=headers)
        self.raise_from_response(r)
        return ServicesDict.model_validate(r.json())

    def get_logs(
        self,
        subscription_uuid: str | UUID,
        direction: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        from_date: str | None = None,
    ) -> SubscriptionLogListResponse:
        """Get logs for a subscription.

        Args:
            subscription_uuid: UUID of the subscription
            direction: Optional sorting direction
            order: Optional ordering field
            limit: Optional maximum number of logs to return
            offset: Optional offset for pagination
            from_date: Optional date to start from

        Returns:
            List of subscription logs

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting logs for subscription %s", subscription_uuid)
        params: dict[str, str | int] = {}
        if direction is not None:
            params["direction"] = direction
        if order is not None:
            params["order"] = order
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if from_date is not None:
            params["from_date"] = from_date

        headers = self._get_headers()
        url = self._client.url(self.resource, str(subscription_uuid), "logs")
        r = self._sync_request("get", url, headers=headers, params=params)
        self.raise_from_response(r)
        return SubscriptionLogListResponse.model_validate(r.json())

    async def get_logs_async(
        self,
        subscription_uuid: str | UUID,
        direction: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        from_date: str | None = None,
    ) -> SubscriptionLogListResponse:
        """Get logs for a subscription asynchronously.

        Args:
            subscription_uuid: UUID of the subscription
            direction: Optional sorting direction
            order: Optional ordering field
            limit: Optional maximum number of logs to return
            offset: Optional offset for pagination
            from_date: Optional date to start from

        Returns:
            List of subscription logs

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting logs for subscription %s (async)", subscription_uuid)
        params: dict[str, str | int] = {}
        if direction is not None:
            params["direction"] = direction
        if order is not None:
            params["order"] = order
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if from_date is not None:
            params["from_date"] = from_date

        headers = self._get_headers()
        url = self._client.url(self.resource, str(subscription_uuid), "logs")
        r = await self._async_request("get", url, headers=headers, params=params)
        self.raise_from_response(r)
        return SubscriptionLogListResponse.model_validate(r.json())
