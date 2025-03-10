# Copyright 2025 Accent Communications

"""Function keys command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand
from accent_confd_client.relations import UserFuncKeyRelation
from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class TemplateRelation:
    """Relations for function key templates."""

    def __init__(self, builder: Any, template_id: str) -> None:
        """Initialize template relations.

        Args:
            builder: Client instance
            template_id: Template ID

        """
        self.template_id = template_id
        self.user_funckey = UserFuncKeyRelation(builder)

    def add_user(self, user_id: str) -> None:
        """Add a user to the template.

        Args:
            user_id: User ID

        """
        self.user_funckey.associate_funckey_template(user_id, self.template_id)

    async def add_user_async(self, user_id: str) -> None:
        """Add a user to the template asynchronously.

        Args:
            user_id: User ID

        """
        await self.user_funckey.associate_funckey_template_async(
            user_id, self.template_id
        )

    def remove_user(self, user_id: str) -> None:
        """Remove a user from the template.

        Args:
            user_id: User ID

        """
        self.user_funckey.dissociate_funckey_template(user_id, self.template_id)

    async def remove_user_async(self, user_id: str) -> None:
        """Remove a user from the template asynchronously.

        Args:
            user_id: User ID

        """
        await self.user_funckey.dissociate_funckey_template_async(
            user_id, self.template_id
        )


class FuncKeysCommand(CRUDCommand):
    """Command for managing function keys."""

    resource = "funckeys/templates"
    relation_cmd = TemplateRelation

    def get_template_funckey(self, template_id: str, position: str) -> dict[str, Any]:
        """Get a function key for a template.

        Args:
            template_id: Template ID
            position: Position

        Returns:
            Function key data

        """
        url = url_join(self.resource, template_id, position)
        response = self.session.get(url)
        return response.json()

    async def get_template_funckey_async(
        self, template_id: str, position: str
    ) -> dict[str, Any]:
        """Get a function key for a template asynchronously.

        Args:
            template_id: Template ID
            position: Position

        Returns:
            Function key data

        """
        url = url_join(self.resource, template_id, position)
        response = await self.session.get_async(url)
        return response.json()

    def delete_template_funckey(self, template_id: str, position: str) -> None:
        """Delete a function key from a template.

        Args:
            template_id: Template ID
            position: Position

        """
        url = url_join(self.resource, template_id, position)
        self.session.delete(url)

    async def delete_template_funckey_async(
        self, template_id: str, position: str
    ) -> None:
        """Delete a function key from a template asynchronously.

        Args:
            template_id: Template ID
            position: Position

        """
        url = url_join(self.resource, template_id, position)
        await self.session.delete_async(url)

    def update_template_funckey(
        self, template_id: str, position: str, funckey: dict[str, Any]
    ) -> None:
        """Update a function key for a template.

        Args:
            template_id: Template ID
            position: Position
            funckey: Function key data

        """
        url = url_join(self.resource, template_id, position)
        self.session.put(url, funckey)

    async def update_template_funckey_async(
        self, template_id: str, position: str, funckey: dict[str, Any]
    ) -> None:
        """Update a function key for a template asynchronously.

        Args:
            template_id: Template ID
            position: Position
            funckey: Function key data

        """
        url = url_join(self.resource, template_id, position)
        await self.session.put_async(url, funckey)
