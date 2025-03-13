# file: accent_dao/resources/func_key/hint_dao.py
# Copyright 2025 Accent Communications
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from accent.accent_helpers import clean_extension
from sqlalchemy import (
    Integer,
    Unicode,
    and_,
    bindparam,
    func,
    literal_column,
    select,
)
from sqlalchemy.sql.expression import cast

from accent_dao.alchemy.conference import Conference
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.alchemy.func_key_dest_agent import FuncKeyDestAgent
from accent_dao.alchemy.func_key_dest_bsfilter import FuncKeyDestBSFilter
from accent_dao.alchemy.func_key_dest_conference import FuncKeyDestConference
from accent_dao.alchemy.func_key_dest_custom import FuncKeyDestCustom
from accent_dao.alchemy.func_key_dest_forward import FuncKeyDestForward
from accent_dao.alchemy.func_key_dest_group_member import FuncKeyDestGroupMember
from accent_dao.alchemy.func_key_dest_service import FuncKeyDestService
from accent_dao.alchemy.func_key_mapping import FuncKeyMapping
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession, daosession
from accent_dao.resources.func_key.model import Hint

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

user_extension = select(Extension).alias()
user_line = select(UserLine).alias()
line_extension = select(LineExtension).alias()
line_features = select(LineFeatures).alias()

agent_hints_bakery = (
    select(
        FuncKeyDestAgent.agent_id.cast(Unicode).label("argument"),
        UserFeatures.id.label("user_id"),
        FeatureExtension.exten.label("feature_extension"),
        user_extension.c.context,
    )
    .join(
        FeatureExtension,
        FeatureExtension.uuid == FuncKeyDestAgent.feature_extension_uuid,
    )
    .join(
        FuncKeyMapping,
        FuncKeyDestAgent.func_key_id == FuncKeyMapping.func_key_id,
    )
    .filter(
        FeatureExtension.enabled.is_(True),
    )
    .join(
        UserFeatures,
        FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
    )
    .join(
        user_line,
        UserFeatures.id == user_line.c.user_id,
    )
    .join(
        line_extension,
        line_extension.c.line_id == user_line.c.line_id,
    )
    .join(
        user_extension,
        line_extension.c.extension_id == user_extension.c.id,
    )
    .filter(
        user_line.c.main_user.is_(True),
        line_extension.c.main_extension.is_(True),
        FuncKeyMapping.blf.is_(True),
    )
)

bsfilter_hints_bakery = (
    select(
        FuncKeyDestBSFilter.filtermember_id.cast(Unicode).label("argument"),
        Extension.context,
    )
    .join(
        Callfiltermember,
        Callfiltermember.id == FuncKeyDestBSFilter.filtermember_id,
    )
    .join(
        Callfilter,
        Callfilter.id == Callfiltermember.callfilterid,
    )
    .join(
        UserFeatures,
        cast(Callfiltermember.typeval, Integer) == UserFeatures.id,
    )
    .join(
        UserLine,
        UserLine.user_id == UserFeatures.id,
    )
    .join(
        LineExtension,
        UserLine.line_id == LineExtension.line_id,
    )
    .join(
        Extension,
        Extension.id == LineExtension.extension_id,
    )
    .filter(
        UserLine.main_user.is_(True),
        LineExtension.main_extension.is_(True),
        Extension.commented == 0,
        Callfilter.commented == 0,
    )
)


conference_hints_bakery = (
    select(
        Conference.id.label("conference_id"),
        Extension.exten.label("extension"),
        Extension.context,
    )
    .select_from(Conference)
    .join(FuncKeyDestConference, FuncKeyDestConference.conference_id == Conference.id)
    .join(
        Extension,
        and_(
            Extension.type == "conference",
            Extension.typeval == cast(Conference.id, String),
        ),
    )
)

custom_hints_bakery = (
    select(FuncKeyDestCustom.exten.label("extension"), user_extension.c.context)
    .join(
        FuncKeyMapping,
        FuncKeyDestCustom.func_key_id == FuncKeyMapping.func_key_id,
    )
    .join(
        UserFeatures,
        FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
    )
    .join(
        user_line,
        UserFeatures.id == user_line.c.user_id,
    )
    .join(
        line_extension,
        line_extension.c.line_id == user_line.c.line_id,
    )
    .join(
        user_extension,
        line_extension.c.extension_id == user_extension.c.id,
    )
    .filter(
        and_(
            user_line.c.main_user.is_(True),
            line_extension.c.main_extension.is_(True),
            FuncKeyMapping.blf.is_(True),
        )
    )
)

forwards_hints_bakery = (
    select(
        FeatureExtension.exten.label("feature_extension"),
        UserFeatures.id.label("user_id"),
        FuncKeyDestForward.number.label("argument"),
        user_extension.c.context,
    )
    .join(
        FuncKeyDestForward,
        FuncKeyDestForward.feature_extension_uuid == FeatureExtension.uuid,
    )
    .join(
        FuncKeyMapping,
        FuncKeyDestForward.func_key_id == FuncKeyMapping.func_key_id,
    )
    .filter(FeatureExtension.enabled == True)
    .join(
        UserFeatures,
        FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
    )
    .join(
        user_line,
        UserFeatures.id == user_line.c.user_id,
    )
    .join(
        line_extension,
        line_extension.c.line_id == user_line.c.line_id,
    )
    .join(
        user_extension,
        line_extension.c.extension_id == user_extension.c.id,
    )
    .filter(
        and_(
            user_line.c.main_user.is_(True),
            line_extension.c.main_extension.is_(True),
            FuncKeyMapping.blf.is_(True),
        )
    )
)

groupmember_hints_bakery = (
    select(
        cast(FuncKeyDestGroupMember.group_id, Unicode).label("argument"),
        UserFeatures.id.label("user_id"),
        FeatureExtension.exten.label("feature_extension"),
        user_extension.c.context,
    )
    .join(
        FeatureExtension,
        FeatureExtension.uuid == FuncKeyDestGroupMember.feature_extension_uuid,
    )
    .join(
        FuncKeyMapping,
        FuncKeyDestGroupMember.func_key_id == FuncKeyMapping.func_key_id,
    )
    .filter(
        FeatureExtension.enabled == True(),
    )
    .join(
        UserFeatures,
        FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
    )
    .join(
        user_line,
        UserFeatures.id == user_line.c.user_id,
    )
    .join(
        line_extension,
        line_extension.c.line_id == user_line.c.line_id,
    )
    .join(
        user_extension,
        line_extension.c.extension_id == user_extension.c.id,
    )
    .filter(
        and_(
            user_line.c.main_user.is_(True),
            line_extension.c.main_extension.is_(True),
            FuncKeyMapping.blf.is_(True),
        )
    )
)

user_extensions_bakery = (
    select(
        UserFeatures.id.label("user_id"),
        Extension.exten.label("extension"),
        Extension.context,
    )
    .distinct()
    .join(
        UserLine.userfeatures,
    )
    .join(
        LineExtension,
        UserLine.line_id == LineExtension.line_id,
    )
    .join(
        Extension,
        LineExtension.extension_id == Extension.id,
    )
    .filter(
        and_(
            UserLine.main_user.is_(True),
            LineExtension.main_extension.is_(True),
            UserFeatures.enablehint == 1,
        )
    )
)

user_arguments_bakery = (
    select(
        UserFeatures.id.label("user_id"),
        func.string_agg(
            case(
                [
                    (
                        LineFeatures.endpoint_sip_uuid.isnot(None),
                        literal_column("'PJSIP/'") + EndpointSIP.name,
                    ),
                    (
                        LineFeatures.endpoint_sccp_id.isnot(None),
                        literal_column("'SCCP/'") + SCCPLine.name,
                    ),
                    (
                        LineFeatures.endpoint_custom_id.isnot(None),
                        UserCustom.interface,
                    ),
                ]
            ),
            literal_column("'&'"),
        ).label("argument"),
    )
    .join(
        UserLine.userfeatures,
    )
    .join(
        LineFeatures,
    )
    .outerjoin(
        EndpointSIP,
    )
    .outerjoin(
        SCCPLine,
    )
    .outerjoin(
        UserCustom,
    )
    .filter(
        and_(
            UserLine.main_user.is_(True),
            LineFeatures.commented == 0,
        )
    )
    .group_by(UserFeatures.id)
)
user_arguments_bakery += lambda q: q.filter(
    UserFeatures.id.in_(bindparam("user_ids", expanding=True))
)

service_hints_bakery = (
    select(
        FeatureExtension.exten.label("feature_extension"),
        UserFeatures.id.label("user_id"),
        user_extension.c.context,
    )
    .join(
        FuncKeyDestService,
        FuncKeyDestService.feature_extension_uuid == FeatureExtension.uuid,
    )
    .join(
        FuncKeyMapping,
        FuncKeyDestService.func_key_id == FuncKeyMapping.func_key_id,
    )
    .filter(FeatureExtension.enabled == True())
    .join(
        UserFeatures,
        FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
    )
    .join(
        user_line,
        UserFeatures.id == user_line.c.user_id,
    )
    .join(
        line_extension,
        line_extension.c.line_id == user_line.c.line_id,
    )
    .join(
        user_extension,
        line_extension.c.extension_id == user_extension.c.id,
    )
    .filter(
        and_(
            user_line.c.main_user.is_(True),
            line_extension.c.main_extension.is_(True),
            FuncKeyMapping.blf.is_(True),
        )
    )
)

extenfeatures_bakery = select(FeatureExtension.exten)
extenfeatures_query += lambda q: q.filter(
    FeatureExtension.feature == bindparam("feature")
)


def _find_extenfeatures(session, feature):
    result = session.execute(
        extenfeatures_query(session).params(feature=feature)
    ).scalar()
    return result


@daosession
def progfunckey_extension(session: Session) -> str | None:
    """Retrieve the extension for programmable function keys.

    Args:
        session: Database session.

    Returns:
        The cleaned extension string, or None if not found.

    """
    extension = _find_extenfeatures(session, "phoneprogfunckey")
    return clean_extension(extension) if extension else None


@daosession
def calluser_extension(session: Session) -> str | None:
    """Retrieve the extension for the calluser feature.

    Args:
        session: Database session.

    Returns:
        The cleaned extension string, or None if not found.

    """
    extension = _find_extenfeatures(session, "calluser")
    return clean_extension(extension) if extension else None


@async_daosession
async def async_user_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for user extensions.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    user_extensions = (await session.execute(user_extensions_bakery(session))).all()
    if not user_extensions:
        return {}

    user_ids = {user.user_id for user in user_extensions}
    user_arguments_result = await session.execute(
        user_arguments_query(session).params(user_ids=list(user_ids))
    )
    user_arguments = {row.user_id: row.argument for row in user_arguments_result}

    hints: dict[str, list[Hint]] = defaultdict(list)
    for user_id, extension, context in user_extensions:
        argument = user_arguments.get(user_id)
        if argument:
            hints[context].append(
                Hint(user_id=user_id, extension=extension, argument=argument)
            )
    return hints


@async_daosession
async def async_conference_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for conference extensions.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(conference_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(conference_id=row.conference_id, extension=row.extension)
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_service_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for service feature extensions.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(service_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(user_id=row.user_id, extension=row.feature_extension, argument=None)
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_forward_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for forward feature extensions.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(forwards_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(
            user_id=row.user_id,
            extension=clean_extension(row.feature_extension),
            argument=row.argument,
        )
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_agent_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for agent feature extensions.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(agent_hints_query(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(
            user_id=row.user_id,
            extension=clean_extension(row.feature_extension),
            argument=str(row.argument),
        )
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_custom_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for custom function key destinations.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(custom_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(extension=row.extension)
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_bsfilter_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for boss-secretary filter function key destinations.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    bsfilter_extension = clean_extension(
        await async_find_extenfeatures(session, "bsfilter")
    )
    result = await session.execute(bsfilter_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(extension=bsfilter_extension, argument=row.argument)
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_groupmember_hints(session: AsyncSession) -> dict[str, list[Hint]]:
    """Gather hints for group member function key destinations.

    Args:
        session: Database session.

    Returns:
        Dictionary mapping context names to lists of Hint objects.

    """
    result = await session.execute(groupmember_hints_bakery(session))
    rows = result.all()
    hints: dict[str, list[Hint]] = defaultdict(list)
    for row in rows:
        hint = Hint(
            user_id=row.user_id,
            extension=clean_extension(row.feature_extension),
            argument=str(row.argument),
        )
        hints[row.context].append(hint)
    return hints


@async_daosession
async def async_find_extenfeatures(session: AsyncSession, feature: str) -> str | None:
    """Retrieve the extension for a specific feature.

    Args:
        session: The database session.
        feature: The feature name to search for.

    Returns:
        The extension string associated with the feature, or None if not found.

    """
    result = await session.execute(extenfeatures_query(session).params(feature=feature))
    return result.scalar_one_or_none()
