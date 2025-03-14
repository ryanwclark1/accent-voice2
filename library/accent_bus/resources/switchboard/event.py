# Copyright 2023 Accent Communications

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..common.event import MultiUserEvent, TenantEvent
from ..common.types import UUIDStr
from .types import (
    HeldCallDict,
    QueuedCallDict,
    SwitchboardDict,
    SwitchboardFallbackDict,
)


class _SwitchboardMixin:
    def __init__(
        self,
        content: Mapping,
        switchboard_uuid: UUIDStr,
        *args: Any,
    ):
        super().__init__(content, *args)  # type: ignore[call-arg]
        if switchboard_uuid is None:
            raise ValueError('switchboard_uuid must have a value')
        self.switchboard_uuid = str(switchboard_uuid)


class SwitchboardCreatedEvent(_SwitchboardMixin, TenantEvent):
    service = 'confd'
    name = 'switchboard_created'
    routing_key_fmt = 'config.switchboards.{switchboard_uuid}.created'
    required_acl_fmt = 'switchboards.{switchboard_uuid}.created'

    def __init__(
        self,
        switchboard: SwitchboardDict,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(switchboard, switchboard_uuid, tenant_uuid)


class SwitchboardDeletedEvent(_SwitchboardMixin, TenantEvent):
    service = 'confd'
    name = 'switchboard_deleted'
    routing_key_fmt = 'config.switchboards.{switchboard_uuid}.deleted'
    required_acl_fmt = 'switchboards.{switchboard_uuid}.deleted'

    def __init__(
        self,
        switchboard: SwitchboardDict,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(switchboard, switchboard_uuid, tenant_uuid)


class SwitchboardEditedEvent(_SwitchboardMixin, TenantEvent):
    service = 'confd'
    name = 'switchboard_edited'
    routing_key_fmt = 'config.switchboards.{switchboard_uuid}.edited'
    required_acl_fmt = 'switchboards.{switchboard_uuid}.edited'

    def __init__(
        self,
        switchboard: SwitchboardDict,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(switchboard, switchboard_uuid, tenant_uuid)


class SwitchboardFallbackEditedEvent(_SwitchboardMixin, TenantEvent):
    service = 'confd'
    name = 'switchboard_fallback_edited'
    routing_key_fmt = 'config.switchboards.fallbacks.edited'
    required_acl_fmt = 'switchboards.fallbacks.edited'

    def __init__(
        self,
        fallback: SwitchboardFallbackDict,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(fallback, switchboard_uuid, tenant_uuid)


class SwitchboardMemberUserAssociatedEvent(_SwitchboardMixin, MultiUserEvent):
    service = 'confd'
    name = 'switchboard_member_user_associated'
    routing_key_fmt = 'config.switchboards.{switchboard_uuid}.members.users.updated'
    required_acl_fmt = 'switchboards.{switchboard_uuid}.members.users.updated'

    def __init__(
        self,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuids: list[str],
    ):
        content = {
            'switchboard_uuid': str(switchboard_uuid),
            'users': [{'uuid': str(uuid)} for uuid in user_uuids],
        }
        super().__init__(content, switchboard_uuid, tenant_uuid, user_uuids)


class SwitchboardQueuedCallsUpdatedEvent(_SwitchboardMixin, TenantEvent):
    service = 'calld'
    name = 'switchboard_queued_calls_updated'
    routing_key_fmt = 'switchboards.{switchboard_uuid}.calls.queued.updated'
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.queued.updated'

    def __init__(
        self,
        items: list[QueuedCallDict],
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'switchboard_uuid': str(switchboard_uuid),
            'items': items,
        }
        super().__init__(content, switchboard_uuid, tenant_uuid)


class SwitchboardQueuedCallAnsweredEvent(_SwitchboardMixin, TenantEvent):
    service = 'calld'
    name = 'switchboard_queued_call_answered'
    routing_key_fmt = (
        'switchboards.{switchboard_uuid}.calls.queued.{queued_call_id}.answer.updated'
    )
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.queued.{queued_call_id}.answer.updated'

    def __init__(
        self,
        operator_call_id: str,
        queued_call_id: str,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'switchboard_uuid': str(switchboard_uuid),
            'operator_call_id': operator_call_id,
            'queued_call_id': queued_call_id,
        }
        super().__init__(content, switchboard_uuid, tenant_uuid)


class SwitchboardHeldCallsUpdatedEvent(_SwitchboardMixin, TenantEvent):
    service = 'calld'
    name = 'switchboard_held_calls_updated'
    routing_key_fmt = 'switchboards.{switchboard_uuid}.calls.held.updated'
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.held.updated'

    def __init__(
        self,
        items: list[HeldCallDict],
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'switchboard_uuid': str(switchboard_uuid),
            'items': items,
        }
        super().__init__(content, switchboard_uuid, tenant_uuid)


class SwitchboardHeldCallAnsweredEvent(_SwitchboardMixin, TenantEvent):
    service = 'calld'
    name = 'switchboard_held_call_answered'
    routing_key_fmt = (
        'switchboards.{switchboard_uuid}.calls.held.{held_call_id}.answer.updated'
    )
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.held.{held_call_id}.answer.updated'

    def __init__(
        self,
        operator_call_id: str,
        held_call_id: str,
        switchboard_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'switchboard_uuid': str(switchboard_uuid),
            'operator_call_id': operator_call_id,
            'held_call_id': held_call_id,
        }
        super().__init__(content, switchboard_uuid, tenant_uuid)
