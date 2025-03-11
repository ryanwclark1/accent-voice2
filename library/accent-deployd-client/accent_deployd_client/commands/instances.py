# Copyright 2025 Accent Communications

"""Deployd instance management commands.

This module provides commands for managing Deployd instances,
including creating, updating, and deleting instances and credentials.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_deployd_client.command import DeploydCommand
from accent_deployd_client.models import (
    Credential,
    Instance,
    InstanceData,
    InstancesList,
)

logger = logging.getLogger(__name__)


class InstancesCommand(DeploydCommand):
    """Command for managing Deployd instances.

    This command provides methods for creating, retrieving, updating,
    and deleting instances and their credentials.
    """

    resource = "instances"

    async def list(
        self, provider_uuid: str | None = None, **params: Any
    ) -> InstancesList:
        """List instances, optionally filtered by provider.

        Args:
            provider_uuid: Optional provider UUID to filter by
            **params: Additional query parameters

        Returns:
            List of instances with metadata

        Raises:
            DeploydError: If the instances cannot be retrieved

        """
        logger.debug("Listing instances with provider=%s", provider_uuid)
        headers = self._get_headers(**params)

        if provider_uuid:
            url = self._provider_instances_all_url(provider_uuid)
        else:
            url = self._instances_all_url()

        response = await self._process_get_request(url, headers, params)
        return InstancesList(**response)

    # For backward compatibility
    def list_sync(
        self, provider_uuid: str | None = None, **params: Any
    ) -> dict[str, Any]:
        """List instances, optionally filtered by provider (synchronous version).

        Args:
            provider_uuid: Optional provider UUID to filter by
            **params: Additional query parameters

        Returns:
            List of instances as a dictionary

        Raises:
            DeploydError: If the instances cannot be retrieved

        """
        logger.debug("Listing instances with provider=%s (sync)", provider_uuid)
        headers = self._get_headers(**params)

        if provider_uuid:
            url = self._provider_instances_all_url(provider_uuid)
        else:
            url = self._instances_all_url()

        response = self.sync_client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def _create_instance(
        self, url: str, instance_data: dict[str, Any], tenant_uuid: str | None
    ) -> dict[str, Any]:
        """Create an instance with the given data.

        Args:
            url: API endpoint URL
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Created instance data

        Raises:
            DeploydError: If the instance cannot be created

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        return await self._process_post_request(url, instance_data, headers)

    # For backward compatibility
    def _create_instance_sync(
        self, url: str, instance_data: dict[str, Any], tenant_uuid: str | None
    ) -> dict[str, Any]:
        """Create an instance with the given data (synchronous version).

        Args:
            url: API endpoint URL
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Created instance data as a dictionary

        Raises:
            DeploydError: If the instance cannot be created

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.sync_client.post(url, json=instance_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)

        return response.json()

    async def register(
        self, instance_data: dict[str, Any] | InstanceData, tenant_uuid: str | None = None
    ) -> Instance:
        """Register a new instance.

        Args:
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Registered instance object

        Raises:
            DeploydError: If the instance cannot be registered

        """
        logger.debug("Registering new instance")
        url = self._instances_all_url()

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        response = await self._create_instance(url, instance_data, tenant_uuid)
        return Instance(**response)

    # For backward compatibility
    def register_sync(
        self, instance_data: dict[str, Any] | InstanceData, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Register a new instance (synchronous version).

        Args:
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Registered instance data as a dictionary

        Raises:
            DeploydError: If the instance cannot be registered

        """
        logger.debug("Registering new instance (sync)")
        url = self._instances_all_url()

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        return self._create_instance_sync(url, instance_data, tenant_uuid)

    async def create(
        self,
        provider_uuid: str,
        instance_data: dict[str, Any] | InstanceData,
        tenant_uuid: str | None = None
    ) -> Instance:
        """Create a new instance with a specific provider.

        Args:
            provider_uuid: Provider UUID
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Created instance object

        Raises:
            DeploydError: If the instance cannot be created

        """
        logger.debug("Creating instance with provider %s", provider_uuid)
        url = self._provider_instances_all_url(provider_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        response = await self._create_instance(url, instance_data, tenant_uuid)
        return Instance(**response)

    # For backward compatibility
    def create_sync(
        self,
        provider_uuid: str,
        instance_data: dict[str, Any] | InstanceData,
        tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Create a new instance with a specific provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            instance_data: Instance configuration data
            tenant_uuid: Optional tenant UUID

        Returns:
            Created instance data as a dictionary

        Raises:
            DeploydError: If the instance cannot be created

        """
        logger.debug("Creating instance with provider %s (sync)", provider_uuid)
        url = self._provider_instances_all_url(provider_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        return self._create_instance_sync(url, instance_data, tenant_uuid)

    async def get(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> Instance:
        """Get information about a specific instance.

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Instance object with complete data

        Raises:
            DeploydError: If the instance cannot be retrieved

        """
        logger.debug("Getting instance %s", instance_uuid)
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = await self._process_get_request(url, headers)
        return Instance(**response)

    # For backward compatibility
    def get_sync(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get information about a specific instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Instance data as a dictionary

        Raises:
            DeploydError: If the instance cannot be retrieved

        """
        logger.debug("Getting instance %s (sync)", instance_uuid)
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.sync_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def get_accent(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get Accent-specific information about an instance.

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Accent-specific instance data

        Raises:
            DeploydError: If the data cannot be retrieved

        """
        logger.debug("Getting Accent info for instance %s", instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._instances_accent_url(instance_uuid)

        return await self._process_get_request(url, headers)

    # For backward compatibility
    def get_accent_sync(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get Accent-specific information about an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Accent-specific instance data as a dictionary

        Raises:
            DeploydError: If the data cannot be retrieved

        """
        logger.debug("Getting Accent info for instance %s (sync)", instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._instances_accent_url(instance_uuid)

        response = self.sync_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def update(
        self,
        instance_uuid: str,
        instance_data: dict[str, Any] | InstanceData,
        tenant_uuid: str | None = None
    ) -> Instance:
        """Update an existing instance.

        Args:
            instance_uuid: Instance UUID
            instance_data: Updated instance configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated instance object

        Raises:
            DeploydError: If the instance cannot be updated

        """
        logger.debug("Updating instance %s", instance_uuid)
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        response = await self._process_put_request(url, instance_data, headers)
        return Instance(**response)

    # For backward compatibility
    def update_sync(
        self,
        instance_uuid: str,
        instance_data: dict[str, Any] | InstanceData,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            instance_data: Updated instance configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated instance data as a dictionary

        Raises:
            DeploydError: If the instance cannot be updated

        """
        logger.debug("Updating instance %s (sync)", instance_uuid)
        url = self._instances_one_url(instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        # Convert to dict if it's a Pydantic model
        if isinstance(instance_data, InstanceData):
            instance_data = instance_data.model_dump()

        response = self.sync_client.put(url, json=instance_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def _delete_instance(self, url: str, tenant_uuid: str | None) -> None:
        """Delete an instance.

        Args:
            url: API endpoint URL
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be deleted

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        await self._process_delete_request(url, headers)

    # For backward compatibility
    def _delete_instance_sync(self, url: str, tenant_uuid: str | None) -> None:
        """Delete an instance (synchronous version).

        Args:
            url: API endpoint URL
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be deleted

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)

        response = self.sync_client.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    async def unregister(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Unregister an instance.

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be unregistered

        """
        logger.debug("Unregistering instance %s", instance_uuid)
        url = self._instances_one_url(instance_uuid)

        await self._delete_instance(url, tenant_uuid)

    # For backward compatibility
    def unregister_sync(
        self, instance_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Unregister an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be unregistered

        """
        logger.debug("Unregistering instance %s (sync)", instance_uuid)
        url = self._instances_one_url(instance_uuid)

        self._delete_instance_sync(url, tenant_uuid)

    async def delete(
        self, provider_uuid: str, instance_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete an instance from a specific provider.

        Args:
            provider_uuid: Provider UUID
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be deleted

        """
        logger.debug(
            "Deleting instance %s from provider %s", instance_uuid, provider_uuid
        )
        url = self._provider_instances_one_url(
            instance_uuid,
            provider_uuid,
        )

        await self._delete_instance(url, tenant_uuid)

    # For backward compatibility
    def delete_sync(
        self, provider_uuid: str, instance_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        """Delete an instance from a specific provider (synchronous version).

        Args:
            provider_uuid: Provider UUID
            instance_uuid: Instance UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the instance cannot be deleted

        """
        logger.debug(
            "Deleting instance %s from provider %s (sync)", instance_uuid, provider_uuid
        )
        url = self._provider_instances_one_url(
            instance_uuid,
            provider_uuid,
        )

        self._delete_instance_sync(url, tenant_uuid)

    async def get_credential(
        self,
        instance_uuid: str,
        credential_uuid: str,
        tenant_uuid: str | None = None,
    ) -> Credential:
        """Get credential information for an instance.

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Credential object

        Raises:
            DeploydError: If the credential cannot be retrieved

        """
        logger.debug(
            "Getting credential %s for instance %s", credential_uuid, instance_uuid
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        response = await self._process_get_request(url, headers)
        return Credential(**response)

    # For backward compatibility
    def get_credential_sync(
        self,
        instance_uuid: str,
        credential_uuid: str,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Get credential information for an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            tenant_uuid: Optional tenant UUID

        Returns:
            Credential data as a dictionary

        Raises:
            DeploydError: If the credential cannot be retrieved

        """
        logger.debug(
            "Getting credential %s for instance %s (sync)",
            credential_uuid,
            instance_uuid,
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        response = self.sync_client.get(url, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def create_credential(
        self,
        instance_uuid: str,
        credential_data: dict[str, Any],
        tenant_uuid: str | None = None,
    ) -> Credential:
        """Create a new credential for an instance.

        Args:
            instance_uuid: Instance UUID
            credential_data: Credential configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Created credential object

        Raises:
            DeploydError: If the credential cannot be created

        """
        logger.debug("Creating credential for instance %s", instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_all_url(instance_uuid)

        response = await self._process_post_request(url, credential_data, headers)
        return Credential(**response)

    # For backward compatibility
    def create_credential_sync(
        self,
        instance_uuid: str,
        credential_data: dict[str, Any],
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Create a new credential for an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            credential_data: Credential configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Created credential data as a dictionary

        Raises:
            DeploydError: If the credential cannot be created

        """
        logger.debug("Creating credential for instance %s (sync)", instance_uuid)
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_all_url(instance_uuid)

        response = self.sync_client.post(url, json=credential_data, headers=headers)
        if response.status_code != 201:
            self.raise_from_response(response)

        return response.json()

    async def update_credential(
        self,
        instance_uuid: str,
        credential_uuid: str,
        credential_data: dict[str, Any],
        tenant_uuid: str | None = None,
    ) -> Credential:
        """Update an existing credential for an instance.

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            credential_data: Updated credential configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated credential object

        Raises:
            DeploydError: If the credential cannot be updated

        """
        logger.debug(
            "Updating credential %s for instance %s", credential_uuid, instance_uuid
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        response = await self._process_put_request(url, credential_data, headers)
        return Credential(**response)

    # For backward compatibility
    def update_credential_sync(
        self,
        instance_uuid: str,
        credential_uuid: str,
        credential_data: dict[str, Any],
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing credential for an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            credential_data: Updated credential configuration
            tenant_uuid: Optional tenant UUID

        Returns:
            Updated credential data as a dictionary

        Raises:
            DeploydError: If the credential cannot be updated

        """
        logger.debug(
            "Updating credential %s for instance %s (sync)",
            credential_uuid,
            instance_uuid,
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        response = self.sync_client.put(url, json=credential_data, headers=headers)
        if response.status_code != 200:
            self.raise_from_response(response)

        return response.json()

    async def delete_credential(
        self,
        instance_uuid: str,
        credential_uuid: str,
        tenant_uuid: str | None = None,
    ) -> None:
        """Delete a credential from an instance.

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the credential cannot be deleted

        """
        logger.debug(
            "Deleting credential %s from instance %s", credential_uuid, instance_uuid
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        await self._process_delete_request(url, headers)

    # For backward compatibility
    def delete_credential_sync(
        self,
        instance_uuid: str,
        credential_uuid: str,
        tenant_uuid: str | None = None,
    ) -> None:
        """Delete a credential from an instance (synchronous version).

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID
            tenant_uuid: Optional tenant UUID

        Raises:
            DeploydError: If the credential cannot be deleted

        """
        logger.debug(
            "Deleting credential %s from instance %s (sync)",
            credential_uuid,
            instance_uuid,
        )
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._credentials_one_url(instance_uuid, credential_uuid)

        response = self.sync_client.delete(url, headers=headers)
        if response.status_code != 204:
            self.raise_from_response(response)

    def _instances_all_url(self) -> str:
        """Get the URL for all instances.

        Returns:
            URL string

        """
        return self.base_url

    def _instances_one_url(self, instance_uuid: str) -> str:
        """Get the URL for a specific instance.

        Args:
            instance_uuid: Instance UUID

        Returns:
            URL string

        """
        return f"{self._instances_all_url()}/{instance_uuid}"

    def _instances_accent_url(self, instance_uuid: str) -> str:
        """Get the URL for Accent-specific instance information.

        Args:
            instance_uuid: Instance UUID

        Returns:
            URL string

        """
        return f"{self._instances_one_url(instance_uuid)}/accent"

    def _credentials_one_url(self, instance_uuid: str, credential_uuid: str) -> str:
        """Get the URL for a specific credential.

        Args:
            instance_uuid: Instance UUID
            credential_uuid: Credential UUID

        Returns:
            URL string

        """
        return (
            f"{self._instances_all_url()}/{instance_uuid}/credentials/{credential_uuid}"
        )

    def _credentials_all_url(self, instance_uuid: str) -> str:
        """Get the URL for all credentials of an instance.

        Args:
            instance_uuid: Instance UUID

        Returns:
            URL string

        """
        return f"{self._instances_all_url()}/{instance_uuid}/credentials"

    def _provider_instances_all_url(self, provider_uuid: str) -> str:
        """Get the URL for all instances of a provider.

        Args:
            provider_uuid: Provider UUID

        Returns:
            URL string

        """
        return self._client.url("providers", provider_uuid, "instances")

    def _provider_instances_one_url(
        self, instance_uuid: str, provider_uuid: str
    ) -> str:
        """Get the URL for a specific instance of a provider.

        Args:
            instance_uuid: Instance UUID
            provider_uuid: Provider UUID

        Returns:
            URL string

        """
        return f"{self._provider_instances_all_url(provider_uuid)}/{instance_uuid}"
