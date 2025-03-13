# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


class LineFixes:
    """Provides methods to fix inconsistencies in LineFeatures data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize LineFixes with a database session.

        Args:
            session: The database session.

        """
        self.session = session

    @async_daosession
    async def fix(self, session: AsyncSession, line_id: int) -> None:
        """Fix inconsistencies for a specific line.

        Args:
            session: The database session.
            line_id: The ID of the line to fix.

        """
        line = await session.get(
            LineFeatures,
            line_id,
            options=[
                selectinload(LineFeatures.endpoint_sip),
                selectinload(LineFeatures.endpoint_sccp),
                selectinload(LineFeatures.endpoint_custom),
                selectinload(LineFeatures.user_lines).selectinload(
                    UserLine.main_user_rel
                ),  # Load main_user relationship
                selectinload(LineFeatures.line_extensions).selectinload(
                    "main_extension_rel"
                ),
            ],
        )
        if not line:
            logger.warning("Line with ID %s not found for fixing.", line_id)
            return  # Added to avoid the error and follow same logic as other resources

        await self.fix_number_and_context(line)
        await self.fix_protocol(line)
        await self.fix_name(line)
        await self.fix_caller_id(line)
        await session.flush()  # Important: Flush changes

    async def fix_number_and_context(self, line: LineFeatures) -> None:
        """Update the number and context of the line based on the main extension.

        Args:
            line: The line object.

        """
        main_extension = line.main_extension_rel
        if main_extension:
            line.number = main_extension.exten
            line.context = main_extension.context
        else:
            line.number = None

    async def fix_protocol(self, line: LineFeatures) -> None:
        """Update the protocol of the line based on the associated endpoint.

        Args:
            line: The line object.

        """
        if line.endpoint_sip_uuid:
            await self._fix_queue_member(line, f"PJSIP/{line.endpoint_sip.name}")
        elif line.endpoint_sccp_id:
            await self._fix_sccp_line(line)
            await self._fix_queue_member(line, f"SCCP/{line.endpoint_sccp.name}")
        elif line.endpoint_custom_id:
            if line.endpoint_custom:
                line.endpoint_custom.context = line.context
                await self._fix_queue_member(line, line.endpoint_custom.interface)
            else:
                logger.warning(
                    "Custom endpoint with id %s not found, cannot update the line %s",
                    line.endpoint_custom_id,
                    line.id,
                )
        else:  # added to respect the previous logic
            await self._fix_queue_member(line, "")

    async def _fix_sccp_line(self, line: LineFeatures) -> None:
        """Update the SCCP line based on the associated extension.

        Args:
            line: The line object.

        """
        if line.endpoint_sccp:
            if main_extension := line.main_extension_rel:
                line.endpoint_sccp.context = main_extension.context

    async def fix_name(self, line: LineFeatures) -> None:
        """Update the name of the line based on the associated endpoint.

        Args:
            line: The line object.

        """
        if line.endpoint_sip and line.endpoint_sip.name not in ("", None):
            line.name = line.endpoint_sip.name
        elif line.endpoint_sccp and line.endpoint_sccp.name not in ("", None):
            line.name = line.endpoint_sccp.name
        elif line.endpoint_custom and line.endpoint_custom.interface not in ("", None):
            line.name = line.endpoint_custom.interface
        else:
            line.name = None

    async def fix_caller_id(self, line: LineFeatures) -> None:
        """Update the caller ID of the line based on the associated user and extension.

        Args:
            line: The line object.

        """
        main_user = line.main_user_rel
        if main_user:
            if line.endpoint_sip_uuid and line.endpoint_sip:
                await line.endpoint_sip.update_caller_id(
                    main_user, line.main_extension_rel
                )
            elif line.endpoint_sccp_id and line.endpoint_sccp:
                line.endpoint_sccp.update_caller_id(main_user, line.main_extension_rel)

    async def _fix_queue_member(self, line: LineFeatures, interface: str) -> None:
        """Update the queue member interface based on the line and user.

        Args:
            line: The line object.
            interface: The interface string.

        """
        # Use a separate method to avoid making changes if the line don't need change
        if not line.main_user_rel:
            return
        stmt = (
            select(QueueMember)
            .where(QueueMember.usertype == "user")
            .where(QueueMember.userid == line.main_user_rel.id)
            .where(QueueMember.interface != interface)
        )
        result = await self.session.execute(stmt)
        queue_members_to_update = result.scalars().all()

        for queue_member in queue_members_to_update:
            # Check interface prefix and act accordingly.
            if queue_member.interface.startswith("Local/") and line.main_extension_rel:
                queue_member.interface = f"Local/{line.main_extension_rel.exten}@{line.main_extension_rel.context}"
            elif (
                queue_member.interface.startswith("PJSIP/")
                or queue_member.interface.startswith("SCCP/")
                or queue_member.interface.startswith("CUSTOM/")
                or queue_member.interface.startswith("Local/")
            ):
                queue_member.interface = interface
