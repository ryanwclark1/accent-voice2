# asterisk_conf_dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    NamedTuple,
)

from sqlalchemy import and_, func, literal, or_, select
from sqlalchemy import cast as sql_cast
from sqlalchemy.types import Integer

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.alchemy.features import Features
from accent_dao.alchemy.func_key_dest_custom import FuncKeyDestCustom
from accent_dao.alchemy.func_key_mapping import FuncKeyMapping
from accent_dao.alchemy.groupfeatures import GroupFeatures
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.pickup import Pickup
from accent_dao.alchemy.pickupmember import PickupMember
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.sccpdevice import SCCPDevice
from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.alchemy.voicemail import Voicemail
from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.ext.asyncio import AsyncSession



class Member(NamedTuple):
    """Represents a queue member."""

    interface: str
    penalty: str
    name: str
    state_interface: str


@async_daosession
async def find_sccp_general_settings(session: AsyncSession) -> list[dict[str, str]]:
    """Find SCCP general settings (async version).

    Args:
        session: Async database session

    Returns:
        List of general settings

    """
    # Get all SCCP general settings
    stmt = select(SCCPGeneralSettings)
    result = await session.execute(stmt)
    rows = result.scalars().all()

    # Get voicemail consult extension
    vmexten_stmt = select(
        literal("vmexten").label("option_name"),
        FeatureExtension.exten.label("option_value"),
    ).filter(
        FeatureExtension.feature == "vmusermsg",
    )
    vmexten_result = await session.execute(vmexten_stmt)
    voicemail_consult_exten = vmexten_result.first()

    # Prepare result
    res = [
        {
            "option_name": row.option_name,
            "option_value": row.option_value,
        }
        for row in rows
    ]

    res.append(
        {
            "option_name": voicemail_consult_exten.option_name,
            "option_value": voicemail_consult_exten.option_value,
        }
    )

    return res


@async_daosession
async def find_sccp_line_settings(session: AsyncSession) -> list[dict[str, Any]]:
    """Find SCCP line settings (async version).

    Args:
        session: Async database session

    Returns:
        List of dictionaries with line settings

    """
    sccp_pickup_members = await async_find_pickup_members(session, "sccp")

    def line_config(*args: Any) -> dict[str, Any]:
        (
            endpoint_sccp_id,
            tenant_uuid,
            name,
            cid_name,
            cid_num,
            allow,
            disallow,
            language,
            user_id,
            context,
            number,
            uuid,
            enable_online_recording,
        ) = args

        line = {
            "id": endpoint_sccp_id,
            "name": name,
            "cid_name": cid_name,
            "cid_num": cid_num,
            "user_id": user_id,
            "number": number,
            "context": context,
            "language": language,
            "uuid": uuid,
            "tenant_uuid": tenant_uuid,
            "enable_online_recording": enable_online_recording,
        }

        if allow:
            line["allow"] = allow
        if disallow:
            line["disallow"] = disallow

        line.update(sccp_pickup_members.get(endpoint_sccp_id, {}))

        return line

    # Use modern SQLAlchemy 2.0 style query
    stmt = (
        select(
            SCCPLine.id,
            SCCPLine.tenant_uuid,
            SCCPLine.name,
            SCCPLine.cid_name,
            SCCPLine.cid_num,
            SCCPLine.allow,
            SCCPLine.disallow,
            UserFeatures.language,
            UserLine.user_id,
            LineFeatures.context,
            Extension.exten,
            UserFeatures.uuid,
            UserFeatures.enableonlinerec,
        )
        .join(
            LineFeatures,
            and_(
                LineFeatures.endpoint_sccp_id == SCCPLine.id,
            ),
        )
        .join(
            UserLine,
            UserLine.line_id == LineFeatures.id,
        )
        .join(
            UserFeatures,
            and_(
                UserFeatures.id == UserLine.user_id,
                UserLine.main_user.is_(True),
            ),
        )
        .join(
            LineExtension,
            and_(
                LineFeatures.id == LineExtension.line_id,
                LineExtension.main_extension.is_(True),
            ),
        )
        .join(
            Extension,
            LineExtension.extension_id == Extension.id,
        )
        .filter(LineFeatures.commented == 0)
    )

    result = await session.execute(stmt)
    rows = result.all()

    return [line_config(*row) for row in rows]


@async_daosession
async def find_sccp_device_settings(
    session: AsyncSession,
) -> list[dict[str, Any]]:
    """Find SCCP device settings (async version).

    Args:
        session: Async database session

    Returns:
        List of dictionaries with device settings

    """
    # Use modern SQLAlchemy 2.0 style query
    stmt = (
        select(
            SCCPDevice,
            Voicemail.mailbox,
        )
        .outerjoin(
            SCCPLine,
            SCCPLine.name == SCCPDevice.line,
        )
        .outerjoin(
            LineFeatures,
            and_(
                LineFeatures.endpoint_sccp_id == SCCPLine.id,
            ),
        )
        .outerjoin(
            UserLine,
            and_(
                UserLine.line_id == LineFeatures.id,
                UserLine.main_user.is_(True),
            ),
        )
        .outerjoin(
            UserFeatures,
            UserFeatures.id == UserLine.user_id,
        )
        .outerjoin(
            Voicemail,
            Voicemail.uniqueid == UserFeatures.voicemailid,
        )
    )

    result = await session.execute(stmt)
    rows = result.all()

    devices = []
    for row in rows:
        device = row.SCCPDevice.todict()
        device["voicemail"] = row.mailbox
        devices.append(device)

    return devices


@async_daosession
async def find_sccp_speeddial_settings(
    session: AsyncSession,
) -> list[dict[str, Any]]:
    """Find SCCP speeddial settings (async version).

    Args:
        session: Async database session

    Returns:
        List of dictionaries with speeddial settings

    """
    invalid_chars = "\n\r\t;"

    # Use modern SQLAlchemy 2.0 style query
    stmt = (
        select(
            FuncKeyMapping.position.label("fknum"),
            func.translate(FuncKeyMapping.label, invalid_chars, "").label("label"),
            sql_cast(FuncKeyMapping.blf, Integer).label("supervision"),
            func.translate(FuncKeyDestCustom.exten, invalid_chars, "").label("exten"),
            UserFeatures.id.label("user_id"),
            SCCPDevice.device.label("device"),
        )
        .join(
            UserFeatures,
            FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
        )
        .join(
            FuncKeyDestCustom,
            FuncKeyDestCustom.func_key_id == FuncKeyMapping.func_key_id,
        )
        .join(
            UserLine,
            and_(
                UserLine.user_id == UserFeatures.id,
                UserLine.main_user.is_(True),
            ),
        )
        .join(
            LineFeatures,
            UserLine.line_id == LineFeatures.id,
        )
        .join(
            SCCPLine,
            and_(
                LineFeatures.endpoint_sccp_id == SCCPLine.id,
            ),
        )
        .join(
            SCCPDevice,
            SCCPLine.name == SCCPDevice.line,
        )
        .filter(LineFeatures.commented == 0)
    )

    result = await session.execute(stmt)
    rows = result.all()

    return [
        {
            "exten": row.exten,
            "fknum": row.fknum,
            "label": row.label,
            "supervision": row.supervision,
            "user_id": row.user_id,
            "device": row.device,
        }
        for row in rows
    ]



@async_daosession
async def find_features_settings(
    session: AsyncSession,
) -> dict[str, list[tuple[str, str]]]:
    """Find features settings (async version).

    Args:
        session: Async database session

    Returns:
        Dictionary with feature settings

    """
    # Use modern SQLAlchemy 2.0 style query
    stmt = select(
        Features.category,
        Features.var_name,
        Features.var_val,
    ).filter(
        and_(
            Features.commented == 0,
            or_(
                Features.category == "general",
                Features.category == "featuremap",
                Features.category == "applicationmap",
            ),
        )
    )

    result = await session.execute(stmt)
    rows = result.all()

    general_options = []
    featuremap_options = []
    applicationmap_options = []
    for row in rows:
        option = (row.var_name, row.var_val)
        if row.category == "general":
            general_options.append(option)
        elif row.category == "applicationmap":
            applicationmap_options.append(option)
        elif row.category == "featuremap":
            featuremap_options.append(option)
            if row.var_name == "disconnect":
                option = ("atxferabort", row.var_val)
                general_options.append(option)

    return {
        "general_options": general_options,
        "featuremap_options": featuremap_options,
        "applicationmap_options": applicationmap_options,
    }



@async_daosession
async def find_pickup_members(
    session: AsyncSession, protocol: str
) -> dict[Any, dict[str, set]]:
    """Find pickup members (async version).

    Args:
        session: Async database session
        protocol: Protocol to filter by

    Returns:
        Dictionary of pickup members

    """
    group_map = {
        "member": "pickupgroup",
        "pickup": "callgroup",
    }

    res = defaultdict(lambda: defaultdict(set))

    def _add_member(m: Any) -> None:
        if protocol == "sip":
            res_base = res[m.endpoint_sip_uuid]
        elif protocol == "sccp":
            res_base = res[m.endpoint_sccp_id]
        elif protocol == "custom":
            res_base = res[m.endpoint_custom_id]
        res_base[group_map[m.category]].add(m.id)

    add_member = _add_member

    # Base query parts
    base_select = [
        PickupMember.category,
        Pickup.id,
        LineFeatures.endpoint_sip_uuid,
        LineFeatures.endpoint_sccp_id,
        LineFeatures.endpoint_custom_id,
    ]

    base_join = (
        select(*base_select)
        .join(
            Pickup,
            Pickup.id == PickupMember.pickupid,
        )
        .filter(Pickup.commented == 0)
    )

    # Protocol-specific filtering
    if protocol == "sip":
        base_join = base_join.filter(LineFeatures.endpoint_sip_uuid.isnot(None))
    elif protocol == "sccp":
        base_join = base_join.filter(LineFeatures.endpoint_sccp_id.isnot(None))
    elif protocol == "custom":
        base_join = base_join.filter(LineFeatures.endpoint_custom_id.isnot(None))

    # Users query
    users_stmt = (
        base_join.join(
            UserLine,
            UserLine.user_id == PickupMember.memberid,
        )
        .join(
            LineFeatures,
            LineFeatures.id == UserLine.line_id,
        )
        .filter(
            PickupMember.membertype == "user",
        )
    )

    # Groups query
    groups_stmt = (
        base_join.join(
            GroupFeatures,
            GroupFeatures.id == PickupMember.memberid,
        )
        .join(
            QueueMember,
            QueueMember.queue_name == GroupFeatures.name,
        )
        .join(
            UserLine,
            UserLine.user_id == QueueMember.userid,
        )
        .join(
            LineFeatures,
            LineFeatures.id == UserLine.line_id,
        )
        .filter(
            and_(
                PickupMember.membertype == "group",
                QueueMember.usertype == "user",
                UserLine.main_user.is_(True),
                UserLine.main_line.is_(True),
            )
        )
    )

    # Queues query
    queues_stmt = (
        base_join.join(
            QueueFeatures,
            QueueFeatures.id == PickupMember.memberid,
        )
        .join(
            QueueMember,
            QueueMember.queue_name == QueueFeatures.name,
        )
        .join(
            UserLine,
            UserLine.user_id == QueueMember.userid,
        )
        .join(
            LineFeatures,
            LineFeatures.id == UserLine.line_id,
        )
        .filter(
            and_(
                PickupMember.membertype == "queue",
                QueueMember.usertype == "user",
                UserLine.main_user.is_(True),
                UserLine.main_line.is_(True),
            )
        )
    )

    # Execute all queries and process results
    users_result = await session.execute(users_stmt)
    groups_result = await session.execute(groups_stmt)
    queues_result = await session.execute(queues_stmt)

    all_members = (
        list(users_result.all()) + list(groups_result.all()) + list(queues_result.all())
    )

    for member in all_members:
        add_member(member)

    return dict(res)
