# Copyright 2025 Accent Communications

"""Lines command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    LineApplicationRelation,
    LineDeviceRelation,
    LineEndpointCustomRelation,
    LineEndpointSccpRelation,
    LineEndpointSipRelation,
    LineExtensionRelation,
    UserLineRelation,
)
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class LineRelation:
    """Relations for lines."""

    def __init__(self, builder: Any, line_id: str) -> None:
        """Initialize line relations.

        Args:
            builder: Client instance
            line_id: Line ID

        """
        self.line_id = line_id
        self.user_line = UserLineRelation(builder)
        self.line_application = LineApplicationRelation(builder)
        self.line_extension = LineExtensionRelation(builder)
        self.line_endpoint_sip = LineEndpointSipRelation(builder)
        self.line_endpoint_sccp = LineEndpointSccpRelation(builder)
        self.line_endpoint_custom = LineEndpointCustomRelation(builder)
        self.line_device = LineDeviceRelation(builder)

    @extract_id
    def add_extension(self, extension_id: str) -> Any:
        """Add an extension to the line.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.line_extension.associate(self.line_id, extension_id)

    @extract_id
    async def add_extension_async(self, extension_id: str) -> Any:
        """Add an extension to the line asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.line_extension.associate_async(self.line_id, extension_id)

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the line.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.line_extension.dissociate(self.line_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the line asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.line_extension.dissociate_async(self.line_id, extension_id)

    @extract_id
    def add_user(self, user_id: str) -> Any:
        """Add a user to the line.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return self.user_line.associate(user_id, self.line_id)

    @extract_id
    async def add_user_async(self, user_id: str) -> Any:
        """Add a user to the line asynchronously.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return await self.user_line.associate_async(user_id, self.line_id)

    @extract_id
    def remove_user(self, user_id: str) -> Any:
        """Remove a user from the line.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return self.user_line.dissociate(user_id, self.line_id)

    @extract_id
    async def remove_user_async(self, user_id: str) -> Any:
        """Remove a user from the line asynchronously.

        Args:
            user_id: User ID

        Returns:
            API response

        """
        return await self.user_line.dissociate_async(user_id, self.line_id)

    @extract_id
    def add_endpoint_sip(self, endpoint_sip_id: str) -> Any:
        """Add a SIP endpoint to the line.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_sip.associate(self.line_id, endpoint_sip_id)

    @extract_id
    async def add_endpoint_sip_async(self, endpoint_sip_id: str) -> Any:
        """Add a SIP endpoint to the line asynchronously.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_sip.associate_async(
            self.line_id, endpoint_sip_id
        )

    @extract_id
    def remove_endpoint_sip(self, endpoint_sip_id: str) -> Any:
        """Remove a SIP endpoint from the line.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_sip.dissociate(self.line_id, endpoint_sip_id)

    @extract_id
    async def remove_endpoint_sip_async(self, endpoint_sip_id: str) -> Any:
        """Remove a SIP endpoint from the line asynchronously.

        Args:
            endpoint_sip_id: SIP endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_sip.dissociate_async(
            self.line_id, endpoint_sip_id
        )

    @extract_id
    def add_endpoint_sccp(self, endpoint_sccp_id: str) -> Any:
        """Add an SCCP endpoint to the line.

        Args:
            endpoint_sccp_id: SCCP endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_sccp.associate(self.line_id, endpoint_sccp_id)

    @extract_id
    async def add_endpoint_sccp_async(self, endpoint_sccp_id: str) -> Any:
        """Add an SCCP endpoint to the line asynchronously.

        Args:
            endpoint_sccp_id: SCCP endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_sccp.associate_async(
            self.line_id, endpoint_sccp_id
        )

    @extract_id
    def remove_endpoint_sccp(self, endpoint_sccp_id: str) -> Any:
        """Remove an SCCP endpoint from the line.

        Args:
            endpoint_sccp_id: SCCP endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_sccp.dissociate(self.line_id, endpoint_sccp_id)

    @extract_id
    async def remove_endpoint_sccp_async(self, endpoint_sccp_id: str) -> Any:
        """Remove an SCCP endpoint from the line asynchronously.

        Args:
            endpoint_sccp_id: SCCP endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_sccp.dissociate_async(
            self.line_id, endpoint_sccp_id
        )

    @extract_id
    def add_endpoint_custom(self, endpoint_custom_id: str) -> Any:
        """Add a custom endpoint to the line.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_custom.associate(self.line_id, endpoint_custom_id)

    @extract_id
    async def add_endpoint_custom_async(self, endpoint_custom_id: str) -> Any:
        """Add a custom endpoint to the line asynchronously.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_custom.associate_async(
            self.line_id, endpoint_custom_id
        )

    @extract_id
    def remove_endpoint_custom(self, endpoint_custom_id: str) -> Any:
        """Remove a custom endpoint from the line.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return self.line_endpoint_custom.dissociate(self.line_id, endpoint_custom_id)

    @extract_id
    async def remove_endpoint_custom_async(self, endpoint_custom_id: str) -> Any:
        """Remove a custom endpoint from the line asynchronously.

        Args:
            endpoint_custom_id: Custom endpoint ID

        Returns:
            API response

        """
        return await self.line_endpoint_custom.dissociate_async(
            self.line_id, endpoint_custom_id
        )

    @extract_id
    def add_device(self, device_id: str) -> Any:
        """Add a device to the line.

        Args:
            device_id: Device ID

        Returns:
            API response

        """
        return self.line_device.associate(self.line_id, device_id)

    @extract_id
    async def add_device_async(self, device_id: str) -> Any:
        """Add a device to the line asynchronously.

        Args:
            device_id: Device ID

        Returns:
            API response

        """
        return await self.line_device.associate_async(self.line_id, device_id)

    @extract_id
    def remove_device(self, device_id: str) -> Any:
        """Remove a device from the line.

        Args:
            device_id: Device ID

        Returns:
            API response

        """
        return self.line_device.dissociate(self.line_id, device_id)

    @extract_id
    async def remove_device_async(self, device_id: str) -> Any:
        """Remove a device from the line asynchronously.

        Args:
            device_id: Device ID

        Returns:
            API response

        """
        return await self.line_device.dissociate_async(self.line_id, device_id)

    def get_device(self) -> dict[str, Any]:
        """Get the device for the line.

        Returns:
            Device data

        """
        return self.line_device.get_by_line(self.line_id)

    async def get_device_async(self) -> dict[str, Any]:
        """Get the device for the line asynchronously.

        Returns:
            Device data

        """
        return await self.line_device.get_by_line_async(self.line_id)

    @extract_id
    def add_application(self, application_uuid: str) -> Any:
        """Add an application to the line.

        Args:
            application_uuid: Application UUID

        Returns:
            API response

        """
        return self.line_application.associate(self.line_id, application_uuid)

    @extract_id
    async def add_application_async(self, application_uuid: str) -> Any:
        """Add an application to the line asynchronously.

        Args:
            application_uuid: Application UUID

        Returns:
            API response

        """
        return await self.line_application.associate_async(
            self.line_id, application_uuid
        )

    @extract_id
    def remove_application(self, application_uuid: str) -> Any:
        """Remove an application from the line.

        Args:
            application_uuid: Application UUID

        Returns:
            API response

        """
        return self.line_application.dissociate(self.line_id, application_uuid)

    @extract_id
    async def remove_application_async(self, application_uuid: str) -> Any:
        """Remove an application from the line asynchronously.

        Args:
            application_uuid: Application UUID

        Returns:
            API response

        """
        return await self.line_application.dissociate_async(
            self.line_id, application_uuid
        )


class LinesCommand(MultiTenantCommand):
    """Command for managing lines."""

    resource = "lines"
    relation_cmd = LineRelation
