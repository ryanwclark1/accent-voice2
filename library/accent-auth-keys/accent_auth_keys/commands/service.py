# Copyright 2025 Accent Communications

"""Service management commands for Accent Auth Keys."""

import asyncio
import logging
import uuid
from typing import Any

from cliff.command import Command

# Configure logging
logger = logging.getLogger(__name__)

POLICY_NAME_TPL = "{username}-internal"


class ServiceUpdate(Command):
    """Update or create all users defined in the config file.

    This command creates or updates services (internal users) and their
    associated policies based on the configuration.
    """

    def get_parser(self, *args: Any, **kwargs: Any) -> Any:
        """Get the argument parser for this command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The configured argument parser.

        """
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            "--recreate",
            help="Delete service before updating it",
            action="store_true",
        )
        return parser

    def take_action(self, parsed_args: Any) -> None:
        """Execute the command.

        Args:
            parsed_args: The parsed command line arguments.

        """
        self.app.LOG.debug("Parsed args: %s", parsed_args)

        # Run the async operations
        asyncio.run(self._async_take_action(parsed_args))

    async def _async_take_action(self, parsed_args: Any) -> None:
        """Execute the command asynchronously.

        Args:
            parsed_args: The parsed command line arguments.

        """
        for name, values in self.app.services.items():
            if parsed_args.recreate:
                await self._delete_service(name)
                await self._delete_policy(name)
                await self.app.file_manager.remove(name)

            service_uuid = await self._find_service_uuid(name)
            if not await self.app.file_manager.service_exists(name):
                if service_uuid:
                    raise RuntimeError(
                        f"User ({name}) exists but not the file associated. Please use '--recreate' option"
                    )
                password = str(uuid.uuid4())
                service_uuid = await self._create_service(name, password)
                await self.app.file_manager.update(name, password)
            elif not service_uuid:
                raise RuntimeError(
                    f"File exists but not the user ({name}) associated. Please use '--recreate' option"
                )

            await self._create_or_update_service_policy(
                name, service_uuid, values["acl"]
            )
            await self.app.file_manager.update_ownership(name, values["system_user"])

    async def _find_service_uuid(self, name: str) -> str | None:
        """Find the UUID of a service by name.

        Args:
            name: The name of the service to find.

        Returns:
            The UUID of the service if found, None otherwise.

        """
        response = await self.app.client.users.list(username=name)
        services = response.items
        for service in services:
            return service["uuid"]
        return None

    async def _delete_service(self, name: str) -> None:
        """Delete a service by name.

        Args:
            name: The name of the service to delete.

        """
        service_uuid = await self._find_service_uuid(name)
        if not service_uuid:
            return

        await self.app.client.users.delete(service_uuid)

    async def _create_service(self, name: str, password: str) -> str:
        """Create a new service.

        Args:
            name: The name of the service to create.
            password: The password for the new service.

        Returns:
            The UUID of the created service.

        """
        service = await self.app.client.users.new(
            username=name, password=password, purpose="internal"
        )
        return service.uuid

    async def _find_policy(self, name: str) -> dict[str, Any] | None:
        """Find a policy by name.

        Args:
            name: The name of the policy to find.

        Returns:
            The policy if found, None otherwise.

        """
        response = await self.app.client.policies.list(name=name)
        policies = response.items
        for policy in policies:
            return policy
        return None

    async def _delete_policy(self, username: str) -> None:
        """Delete a policy associated with a username.

        Args:
            username: The username associated with the policy to delete.

        """
        name = POLICY_NAME_TPL.format(username=username)
        policy = await self._find_policy(name)
        if not policy:
            return

        await self.app.client.policies.delete(policy["uuid"])

    async def _create_or_update_service_policy(
        self, username: str, service_uuid: str, acl: list[str]
    ) -> None:
        """Create or update a policy for a service.

        Args:
            username: The username of the service.
            service_uuid: The UUID of the service.
            acl: The access control list for the policy.

        """
        name = POLICY_NAME_TPL.format(username=username)
        policy = await self._find_policy(name)
        if not policy:
            policy_obj = await self.app.client.policies.new(name, acl=acl)
            await self.app.client.users.add_policy(service_uuid, policy_obj.uuid)
            return

        if sorted(policy["acl"]) == sorted(acl):
            return
        await self.app.client.policies.edit(policy["uuid"], name, acl=acl)


class ServiceClean(Command):
    """Clean undefined files.

    This command cleans up service files and optionally users that are not
    defined in the configuration.
    """

    def get_parser(self, *args: Any, **kwargs: Any) -> Any:
        """Get the argument parser for this command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The configured argument parser.

        """
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            "--users",
            help="Delete undefined internal users",
            action="store_true",
        )
        return parser

    def take_action(self, parsed_args: Any) -> None:
        """Execute the command.

        Args:
            parsed_args: The parsed command line arguments.

        """
        # Run the async operations
        asyncio.run(self._async_take_action(parsed_args))

    async def _async_take_action(self, parsed_args: Any) -> None:
        """Execute the command asynchronously.

        Args:
            parsed_args: The parsed command line arguments.

        """
        excludes = list(self.app.services.keys())
        if parsed_args.users:
            self.app.LOG.debug("Delete all undefined internal users")
            await self._delete_services(excludes)

        await self.app.file_manager.clean(excludes=excludes)

    async def _delete_services(self, excludes: list[str] | None = None) -> None:
        """Delete services not in the excludes list.

        Args:
            excludes: List of service names to exclude from deletion.

        """
        excludes = excludes or []
        excludes.append("accent-auth-cli")
        response = await self.app.client.users.list(purpose="internal")
        services = response.items
        for service in services:
            if service["username"] in excludes:
                continue

            response = await self.app.client.users.get_policies(service["uuid"])
            policies = response.items
            for policy in policies:
                self.app.LOG.debug("Deleting policy: %s", policy["name"])
                await self.app.client.policies.delete(policy["uuid"])
            self.app.LOG.debug("Deleting user: %s", service["username"])
            await self.app.client.users.delete(service["uuid"])
