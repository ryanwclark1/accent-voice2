# file: accent_dao/resources/call_permission/strategy.py
# Copyright 2025 Accent Communications

from sqlalchemy.orm import selectinload

from accent_dao.alchemy.rightcall import RightCall as CallPermission
from accent_dao.alchemy.rightcallmember import RightCallMember

preload_relationships = (
    selectinload(CallPermission.rightcall_groups)
    .selectinload(RightCallMember.group)
    .load_only(
        "uuid", "id", "name"
    ),  # Use attribute, not literal strings.  This was the main error.
    selectinload(CallPermission.rightcall_users)
    .selectinload(RightCallMember.user)
    .load_only("uuid", "firstname", "webi_lastname"),
    selectinload(CallPermission.rightcall_outcalls)
    .selectinload(RightCallMember.outcall)
    .load_only("id", "name"),
    selectinload(CallPermission.rightcallextens),
)
