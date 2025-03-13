# file: accent_dao/resources/line/fixes.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures as Line
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.user_line import UserLine

logger = logging.getLogger(__name__)


class LineFixes:
    """Provides methods for fixing inconsistencies in Line-related data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize LineFixes.

        Args:
            session: The database session.

        """
        self.session = session

    async def async_fix(self, line_id: int) -> None:
        """Fix inconsistencies for a given line.

        Args:
            line_id: The ID of the line to fix.

        """
        await self.async_fix_number_and_context(line_id)
        await self.async_fix_protocol(line_id)
        await self.async_fix_name(line_id)
        await self.async_fix_caller_id(line_id)
        await self.session.flush()

    async def async_fix_number_and_context(self, line_id: int) -> None:
        """Fix the number and context of a line based on its main extension.

        Args:
            line_id: The ID of the line to fix.

        """
        extension = (
            await self.session.execute(
                select(Extension)
                .join(LineExtension, LineExtension.extension_id == Extension.id)
                .where(LineExtension.line_id == line_id)
                .where(LineExtension.main_extension.is_(True))
            )
        ).scalar_one_or_none()

        (
            await self.session.execute(
                update(Line)
                .where(Line.id == line_id)
                .values(
                    number=extension.exten if extension else None,
                    context=extension.context if extension else None,
                )
            )
        )

    async def async_fix_protocol(self, line_id: int) -> None:
        """Fix the protocol of a line based on its associated endpoint.

        Args:
            line_id: The ID of the line to fix.

        """
        line = await self.session.get(Line, line_id)
        if not line:
            return

        if line.endpoint_sip_uuid:
            protocol = "sip"
            interface = f"PJSIP/{line.endpoint_sip.name}"
        elif line.endpoint_sccp_id:
            protocol = "sccp"
            interface = f"SCCP/{line.endpoint_sccp.name}"
        elif line.endpoint_custom_id:
            protocol = "custom"
            interface = line.endpoint_custom.interface
        else:
            return

        await self.session.execute(
            update(Line).where(Line.id == line_id).values(protocol=protocol)
        )
        # also update the interface in any associated queue members
        await self._async_fix_queue_member(user_id, line.name, interface, context)

    async def async_fix_name(self, line_id: int) -> None:
        """Fix the name of a line based on its associated endpoint.

        Args:
            line_id: The ID of the line to fix.

        """
        line = await self.session.get(Line, line_id)
        if not line:
            return

        if line.endpoint_sip and line.endpoint_sip.name:
            new_name = line.endpoint_sip.name
        elif line.endpoint_sccp and line.endpoint_sccp.name:
            new_name = line.endpoint_sccp.name
        elif line.endpoint_custom and line.endpoint_custom.interface:
            new_name = line.endpoint_custom.interface
        else:
            new_name = None

        await self.session.execute(
            update(Line).where(Line.id == line_id).values(name=new_name)
        )

    async def async_fix_caller_id(self, line_id: int) -> None:
        """Fix the caller ID of a line based on its associated user and endpoint.

        Args:
            line_id: The ID of the line to fix.

        """
        line = await self.session.get(Line, line_id)
        if not line:
            return

        user_line = (
            await self.session.execute(
                select(UserLine)
                .filter(UserLine.line_id == line.id)
                .filter(UserLine.main_user.is_(True))
            )
        ).scalar_one_or_none()

        if not user_line:
            return
        user = user_line.user

        if line.endpoint_sip_uuid:
            extension = await self.session.get(
                Extension,
                line.line_extensions[0].extension_id,
            )
            await line.endpoint_sip.update_caller_id(
                user, extension
            )  # Assuming this is already async
        elif line.endpoint_sccp_id:
            extension = await self.session.get(
                Extension,
                line.line_extensions[0].extension_id,
            )
            await line.endpoint_sccp.update_caller_id(
                user, extension
            )  # Assuming this is async.

    async def _async_fix_queue_member(
        self, user_id: int, line_name: str, interface: str, context: str
    ) -> None:
        """Update queue member interface based on user and line.

        Args:
            user_id: ID of the user associated with the queue member.
            line_name: Name of the line.
            interface: Computed interface string.
            context: Context name.

        """
        # Local is a special case, we need to handle the interface differently.
        if interface.startswith("Local/"):
            if user := await self.session.get(User, user_id):
                if main_line := user.main_line:
                    if main_line.line_extensions:
                        extension = main_line.line_extensions[0].extension
                        local_interface = f"Local/{extension.exten}@{extension.context}"
                        (
                            await self.session.execute(
                                update(QueueMember)
                                .where(
                                    QueueMember.usertype == "user",
                                    QueueMember.userid == user_id,
                                    QueueMember.channel == "Local",
                                )
                                .values(interface=local_interface)
                            )
                        )
            return  # Exit early since we updated the local interface

        # For non-local interfaces, update directly
        await self.session.execute(
            update(QueueMember)
            .where(
                QueueMember.usertype == "user",
                QueueMember.userid == user_id,
                QueueMember.interface != interface,
            )
            .values(interface=interface)
        )
