# Copyright 2025 Accent Communications

"""Deployd provider management commands.

This module provides commands for managing Deployd providers,
including creating, updating, and deleting providers.
"""

from __future__ import annotations

import builtins
import logging
from typing import Any

from accent_deployd_client.command import DeploydCommand
from accent_deployd_client.models import (
    Provider,
    ProviderData,
    ProvidersList,
    ResourcesList,
)

logger = logging.getLogger(__name__)


class PlatformsSubcommand(DeploydCommand):
    """Subcommand for provider platforms operations.

    This command provides methods for retrieving platform information.
    """

    resource = "platforms"

    def __init__(self, client: Any, base_url: str) -> None:
        """Initialize the platforms subcommand.

        Args:
            client: The API client
            base_url: Base URL for the platforms endpoint

        """
        super().__init__(client)
        self.base_url = base_url

    async def list(self) -> builtins.list[str]:
        """List available platforms.

        Returns:
            List of platform identifiers

        Raises:
            DeploydError: If the platforms cannot be retrieved

        """
        logger.debug("Listing platforms")
        headers = self._get_headers()
        url = self._providers_platforms_url()

        response = await self.async_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    # For backward compatibility
    def list_sync(self) -> builtins.list[str]:
        """List available platforms (synchronous version).

        Returns:
            List of platform identifiers

        Raises:
            DeploydError: If the platforms cannot be retrieved

        """
        logger.debug("Listing platforms (sync)")
        headers = self._get_headers()
        url = self._providers_platforms_url()

        response = self.sync_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    def _providers_platforms_url(self) -> str:
        """Get the URL for platforms.

        Returns:
            URL string

        """
        return f"{self.base_url}/platforms"


class ProvidersCommand(DeploydCommand):
    """Command for managing Deployd providers.

    This command provides methods for creating, retrieving, updating,
    and deleting providers.
    """

    resource = "providers"

    def __init__(self, client: Any) -> None:
        """Initialize the providers command.

        Args:
            client: The API client

        """
        super().__init__(client)
        self.platforms = PlatformsSubcommand(
            client,
            self.base_url,
        )

    async def list(self, **params: Any) -> ProvidersList:
        """List providers.

        Args:
            **params: Additional query parameters

        Returns:
            List of providers with metadata

        Raises:
            DeploydError: If the providers cannot be retrieved

        """
        logger.debug("Listing providers")
        url = self._providers_all_url()
        headers = self._get_headers(**params)

        response = await self._process_get_request(url, headers, params)
        return ProvidersList(**response)

    # For backward compatibility
    def list_sync(self, **params: Any) -> dict[str, Any]:
        """List providers (synchronous version).

        Args:
            **params: Additional query parameters

        Returns:
            List of providers as a dictionary

        Raises:
            DeploydError: If the providers cannot be retrieved

        """
        logger.debug("Listing providers (sync)")
        url = self._providers_all_url()
        headers = self._get_headers(**params)

        response = self.sync_client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def create(
        self,
        provider_data: dict[str, Any] | ProviderData,
        tenant_uuid: str | None = None,
    ) -> Provider:
        """Create a new provider.

        Args:
            provider_data: Provider configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Created provider object

        Raises:
            DeploydError: If the provider cannot be created

        """
        logger.debug("Creating provider")
        url = self._providers_all_url()
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(provider_data, ProviderData):
            provider_data = provider_data.model_dump()

        response = await self._process_post_request(url, provider_data, headers)
        return Provider(**response)

    # For backward compatibility
    def create_sync(
        self,
        provider_data: dict[str, Any] | ProviderData,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Create a new provider (synchronous version).

        Args:
            provider_data: Provider configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Created provider data as a dictionary

        Raises:
            DeploydError: If the provider cannot be created

        """
        logger.debug("Creating provider (sync)")
        url = self._providers_all_url()
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(provider_data, ProviderData):
            provider_data = provider_data.model_dump()

        response = self.sync_client.post(url, json=provider_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)

        return response.json()

    async def get(
        self, provider_uuid: str, tenant_uuid: str | None = None
    ) -> Provider:
        """Get information about a specific provider.

        Args:
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Provider object with complete data

        Raises:
            DeploydError: If the provider cannot be retrieved

        """
        logger.debug("Getting provider %s", provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        response = await self._process_get_request(url, headers)
        return Provider(**response)

    # For backward compatibility
    def get_sync(
        self, provider_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get information about a specific provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Provider data as a dictionary

        Raises:
            DeploydError: If the provider cannot be retrieved

        """
        logger.debug("Getting provider %s (sync)", provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        response = self.sync_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def update(
        self,
        provider_uuid: str,
        provider_data: dict[str, Any] | ProviderData,
        tenant_uuid: str | None = None,
    ) -> Provider:
        """Update an existing provider.

        Args:
            provider_uuid: Provider UUID
            provider_data: Updated provider configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated provider object

        Raises:
            DeploydError: If the provider cannot be updated

        """
        logger.debug("Updating provider %s", provider_uuid)
        url = self._providers_one_url(provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(provider_data, ProviderData):
            provider_data = provider_data.model_dump()

        response = await self._process_put_request(url, provider_data, headers)
        return Provider(**response)

    # For backward compatibility
    def update_sync(
        self,
        provider_uuid: str,
        provider_data: dict[str, Any] | ProviderData,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            provider_data: Updated provider configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated provider data as a dictionary

        Raises:
            DeploydError: If the provider cannot be updated

        """
        logger.debug("Updating provider %s (sync)", provider_uuid)
        url = self._providers_one_url(provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(provider_data, ProviderData):
            provider_data = provider_data.model_dump()

        response = self.sync_client.put(url, json=provider_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def delete(
        self, provider_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete a provider.

        Args:
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the provider cannot be deleted

        """
        logger.debug("Deleting provider %s", provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        await self._process_delete_request(url, headers)

    # For backward compatibility
    def delete_sync(
        self, provider_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the provider cannot be deleted

        """
        logger.debug("Deleting provider %s (sync)", provider_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._providers_one_url(provider_uuid)

        response = self.sync_client.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    async def list_images(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List images available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of image resources

        Raises:
            DeploydError: If the images cannot be retrieved

        """
        logger.debug("Listing images for provider %s", provider_uuid)
        response = await self._providers_resources("images", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_images_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List images available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of images as a dictionary

        Raises:
            DeploydError: If the images cannot be retrieved

        """
        logger.debug("Listing images for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("images", provider_uuid, **params)

    async def list_locations(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List locations available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of location resources

        Raises:
            DeploydError: If the locations cannot be retrieved

        """
        logger.debug("Listing locations for provider %s", provider_uuid)
        response = await self._providers_resources("locations", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_locations_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List locations available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of locations as a dictionary

        Raises:
            DeploydError: If the locations cannot be retrieved

        """
        logger.debug("Listing locations for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("locations", provider_uuid, **params)

    async def list_key_pairs(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List key pairs available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of key pair resources

        Raises:
            DeploydError: If the key pairs cannot be retrieved

        """
        logger.debug("Listing key pairs for provider %s", provider_uuid)
        response = await self._providers_resources("keypairs", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_key_pairs_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List key pairs available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of key pairs as a dictionary

        Raises:
            DeploydError: If the key pairs cannot be retrieved

        """
        logger.debug("Listing key pairs for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("keypairs", provider_uuid, **params)

    async def list_networks(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List networks available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of network resources

        Raises:
            DeploydError: If the networks cannot be retrieved

        """
        logger.debug("Listing networks for provider %s", provider_uuid)
        response = await self._providers_resources("networks", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_networks_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List networks available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of networks as a dictionary

        Raises:
            DeploydError: If the networks cannot be retrieved

        """
        logger.debug("Listing networks for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("networks", provider_uuid, **params)

    async def list_sizes(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List instance sizes available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of size resources

        Raises:
            DeploydError: If the sizes cannot be retrieved

        """
        logger.debug("Listing sizes for provider %s", provider_uuid)
        response = await self._providers_resources("sizes", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_sizes_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List instance sizes available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of sizes as a dictionary

        Raises:
            DeploydError: If the sizes cannot be retrieved

        """
        logger.debug("Listing sizes for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("sizes", provider_uuid, **params)

    async def list_subnets(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List subnets available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of subnet resources

        Raises:
            DeploydError: If the subnets cannot be retrieved

        """
        logger.debug("Listing subnets for provider %s", provider_uuid)
        response = await self._providers_resources("subnets", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_subnets_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List subnets available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of subnets as a dictionary

        Raises:
            DeploydError: If the subnets cannot be retrieved

        """
        logger.debug("Listing subnets for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("subnets", provider_uuid, **params)

    async def list_regions(self, provider_uuid: str, **params: Any) -> ResourcesList:
        """List regions available for a provider.

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of region resources

        Raises:
            DeploydError: If the regions cannot be retrieved

        """
        logger.debug("Listing regions for provider %s", provider_uuid)
        response = await self._providers_resources("regions", provider_uuid, **params)
        return ResourcesList(**response)

    # For backward compatibility
    def list_regions_sync(self, provider_uuid: str, **params: Any) -> dict[str, Any]:
        """List regions available for a provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            **params: Additional query parameters

        Returns:
            List of regions as a dictionary

        Raises:
            DeploydError: If the regions cannot be retrieved

        """
        logger.debug("Listing regions for provider %s (sync)", provider_uuid)
        return self._providers_resources_sync("regions", provider_uuid, **params)

    def _providers_all_url(self) -> str:
        """Get the URL for all providers.

        Returns:
            URL string

        """
        return self.base_url

    def _providers_one_url(self, provider_uuid: str) -> str:
        """Get the URL for a specific provider.

        Args:
            provider_uuid: Provider UUID

        Returns:
            URL string

        """
        return f"{self._providers_all_url()}/{provider_uuid}"

    async def _providers_resources(
        self,
        endpoint: str,
        provider_uuid: str,
        tenant_uuid: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """Get provider resources by type.

        Args:
            endpoint: Resource type endpoint
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID
            **params: Additional query parameters

        Returns:
            Resource data

        Raises:
            DeploydError: If the resources cannot be retrieved

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self._providers_one_url(provider_uuid)}/{endpoint}"

        return await self._process_get_request(url, headers, params)

    # For backward compatibility
    def _providers_resources_sync(
        self,
        endpoint: str,
        provider_uuid: str,
        tenant_uuid: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """Get provider resources by type (synchronous version).

        Args:
            endpoint: Resource type endpoint
            provider_uuid: Provider UUID
            tenant_uuid: Optional tenant UUID
            **params: Additional query parameters

        Returns:
            Resource data as a dictionary

        Raises:
            DeploydError: If the resources cannot be retrieved

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self._providers_one_url(provider_uuid)}/{endpoint}"

        response = self.sync_client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()
