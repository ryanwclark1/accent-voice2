# Copyright 2025 Accent Communications

"""CRUD command base classes for the Configuration Daemon API."""

import abc
import logging
from typing import Any, Generic, TypeVar

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import extract_id, url_join

# Configure standard logging
logger = logging.getLogger(__name__)

# Type variable for relation command types
R = TypeVar("R")


class CRUDCommand(HTTPCommand, Generic[R]):
    """Base class for CRUD commands."""

    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def resource(self) -> str | list[str]:
        """Get the resource path for the command.

        Returns:
            Resource path or list of path parts

        """
        ...

    @property
    def relation_cmd(self) -> type[R]:
        """Get the relation command class.

        Returns:
            Relation command class

        Raises:
            NotImplementedError: If not implemented by the subclass

        """
        raise NotImplementedError("Command needs to implement an Associator")

    def list(self, **kwargs: Any) -> dict[str, Any]:
        """List resources.

        Args:
            **kwargs: Query parameters

        Returns:
            JSON response

        """
        url = url_join(self.resource)
        response = self.session.get(url, params=kwargs)
        return response.json()

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List resources asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            JSON response

        """
        url = url_join(self.resource)
        response = await self.session.get_async(url, params=kwargs)
        return response.json()

    @extract_id
    def get(self, resource_id: str) -> dict[str, Any]:
        """Get a resource by ID.

        Args:
            resource_id: Resource ID

        Returns:
            JSON response

        """
        url = url_join(self.resource, resource_id)
        response = self.session.get(url)
        return response.json()

    @extract_id
    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get a resource by ID asynchronously.

        Args:
            resource_id: Resource ID

        Returns:
            JSON response

        """
        url = url_join(self.resource, resource_id)
        response = await self.session.get_async(url)
        return response.json()

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a resource.

        Args:
            body: Resource data

        Returns:
            JSON response

        """
        url = url_join(self.resource)
        response = self.session.post(url, body)
        return response.json()

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create a resource asynchronously.

        Args:
            body: Resource data

        Returns:
            JSON response

        """
        url = url_join(self.resource)
        response = await self.session.post_async(url, body)
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update a resource.

        Args:
            body: Resource data

        """
        resource_id = body.get("uuid")
        if not resource_id:
            resource_id = body["id"]
        url = url_join(self.resource, resource_id)
        body = {key: value for key, value in body.items() if key != "links"}
        self.session.put(url, body)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update a resource asynchronously.

        Args:
            body: Resource data

        """
        resource_id = body.get("uuid")
        if not resource_id:
            resource_id = body["id"]
        url = url_join(self.resource, resource_id)
        body = {key: value for key, value in body.items() if key != "links"}
        await self.session.put_async(url, body)

    @extract_id
    def delete(self, resource_id: str) -> None:
        """Delete a resource.

        Args:
            resource_id: Resource ID

        """
        url = url_join(self.resource, resource_id)
        self.session.delete(url)

    @extract_id
    async def delete_async(self, resource_id: str) -> None:
        """Delete a resource asynchronously.

        Args:
            resource_id: Resource ID

        """
        url = url_join(self.resource, resource_id)
        await self.session.delete_async(url)

    @extract_id
    def relations(self, resource_id: str) -> R:
        """Get a relation command for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Relation command instance

        """
        return self.relation_cmd(self._client, resource_id)

    def __call__(self, resource: str | dict[str, Any]) -> R:
        """Call the command as a function.

        Args:
            resource: Resource ID or resource data

        Returns:
            Relation command instance

        """
        return self.relations(resource)


class MultiTenantCommand(CRUDCommand[R]):
    """Base class for multi-tenant CRUD commands."""

    def list(self, **kwargs: Any) -> dict[str, Any]:
        """List resources.

        Args:
            **kwargs: Query parameters

        Returns:
            JSON response

        """
        kwargs.setdefault("recurse", False)
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = self.session.get(url, headers=headers, params=kwargs)
        return response.json()

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List resources asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            JSON response

        """
        kwargs.setdefault("recurse", False)
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.READ_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = await self.session.get_async(url, headers=headers, params=kwargs)
        return response.json()

    @extract_id
    def get(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a resource by ID.

        Args:
            resource_id: Resource ID
            **kwargs: Additional parameters

        Returns:
            JSON response

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, resource_id)
        response = self.session.get(url, headers=headers, params=kwargs)
        return response.json()

    @extract_id
    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get a resource by ID asynchronously.

        Args:
            resource_id: Resource ID
            **kwargs: Additional parameters

        Returns:
            JSON response

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource, resource_id)
        response = await self.session.get_async(url, headers=headers, params=kwargs)
        return response.json()

    def create(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a resource.

        Args:
            body: Resource data
            **kwargs: Additional parameters

        Returns:
            JSON response

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.WRITE_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = self.session.post(url, body, headers=headers)
        return response.json()

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create a resource asynchronously.

        Args:
            body: Resource data
            **kwargs: Additional parameters

        Returns:
            JSON response

        """
        tenant_uuid = kwargs.pop("tenant_uuid", self._client.config.tenant_uuid)
        headers = dict(kwargs.get("headers", self.session.WRITE_HEADERS))
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = await self.session.post_async(url, body, headers=headers)
        return response.json()
