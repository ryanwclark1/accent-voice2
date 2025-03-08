# Copyright 2023 Accent Communications

from sqlalchemy.orm import selectinload

from accent_dao.alchemy.rightcall import RightCall as CallPermission

preload_relationships = (
    selectinload(CallPermission.rightcall_groups)
    .selectinload('group')
    .load_only('uuid', 'id', 'name'),
    selectinload(CallPermission.rightcall_users)
    .selectinload('user')
    .load_only('uuid', 'firstname', 'webi_lastname'),
    selectinload(CallPermission.rightcall_outcalls)
    .selectinload('outcall')
    .load_only('id', 'name'),
    selectinload(CallPermission.rightcallextens),
)
