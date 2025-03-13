# file: accent_dao/resources/user/strategy.py
# Copyright 2025 Accent Communications

from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

user_unpaginated_strategy = (
    joinedload("agent"),
    joinedload("rightcall_members").selectinload("rightcall"),
    joinedload("group_members")
    .selectinload("group")
    .selectinload("call_pickup_interceptor_pickups")
    .options(
        selectinload("pickupmember_user_targets").selectinload("user"),
        selectinload("pickupmember_group_targets")
        .selectinload("group")
        .selectinload("user_queue_members")
        .selectinload("user"),
    ),
    joinedload("call_pickup_interceptor_pickups").options(
        selectinload("pickupmember_user_targets").selectinload("user"),
        selectinload("pickupmember_group_targets")
        .selectinload("group")
        .selectinload("user_queue_members")
        .selectinload("user"),
    ),
    joinedload("user_dialactions").selectinload("user"),
    joinedload("incall_dialactions").selectinload("incall").selectinload("extensions"),
    joinedload("user_lines").options(
        selectinload("line").options(
            selectinload("application"),
            selectinload("context_rel"),
            selectinload("endpoint_sip").options(
                selectinload("_endpoint_section").selectinload("_options"),
                selectinload("_auth_section").selectinload("_options"),
            ),
            selectinload("endpoint_sccp"),
            selectinload("endpoint_custom"),
            selectinload("line_extensions").selectinload("extension"),
            selectinload("user_lines").selectinload("user"),
        ),
    ),
    joinedload("queue_members"),
    joinedload("schedule_paths").selectinload("schedule"),
    joinedload("switchboard_member_users").selectinload("switchboard"),
    joinedload("tenant"),
    joinedload("voicemail"),
    # Don't lazy load anything else, eager load everything specified.
)


no_strategy = []
