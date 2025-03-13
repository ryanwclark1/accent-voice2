# file: accent_dao/resources/directory_profile/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging
from typing import TypedDict

from sqlalchemy import Integer, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


class DirectoryProfile(TypedDict):
    """Represents directory profile information."""

    accent_user_uuid: str
    profile: str


@async_daosession
async def async_find_by_incall_id(
    session: AsyncSession, incall_id: int
) -> DirectoryProfile | None:
    """Find directory profile information by incall ID.

    Args:
        session: The database session.
        incall_id: The ID of the incall.

    Returns:
        A dictionary containing directory profile information,
        or None if not found.

    """
    stmt = (
        select(
            UserFeatures.uuid.label("accent_user_uuid"),
            LineFeatures.context.label("profile"),
        )
        .join(
            Dialaction,
            and_(
                Dialaction.category == "incall",
                Dialaction.categoryval == str(incall_id),
                Dialaction.action == "user",
            ),
        )
        .join(
            UserFeatures,
            and_(
                UserFeatures.id == Dialaction.actionarg1.cast(Integer),
            ),
        )
        .join(
            UserLine,
            and_(
                UserLine.user_id == UserFeatures.id,
                UserLine.main_user.is_(True),
                UserLine.main_line.is_(True),
            ),
        )
        .join(LineFeatures, LineFeatures.id == UserLine.line_id)
    )

    result = await session.execute(stmt)
    row = result.one_or_none()

    if row:
        return {"accent_user_uuid": row.accent_user_uuid, "profile": row.profile}
    return None
