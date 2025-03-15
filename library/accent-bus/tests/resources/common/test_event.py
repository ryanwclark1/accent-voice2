# tests/resources/common/test_event.py
# Copyright 2025 Accent Communications

from uuid import uuid4

import pytest
from accent_bus.resources.common.event import (
    MultiUserEvent,
    ServiceEvent,
    TenantEvent,
    UserEvent,
)

TENANT_UUID = str(uuid4())  # Use str for consistency
USER_UUID = str(uuid4())
USER2_UUID = str(uuid4())
USER3_UUID = str(uuid4())


class SomeServiceEvent(ServiceEvent):
    name = "some_service_event"
    routing_key_fmt = "some.service.event"

    def __init__(self, a, b) -> None:
        content = {"a": a, "b": b}
        super().__init__(content)


class SomeTenantEvent(TenantEvent):
    name = "some_tenant_event"
    routing_key_fmt = "some.tenant.event"

    def __init__(self, a, b, tenant_uuid) -> None:
        content = {"a": a, "b": b}
        super().__init__(content, tenant_uuid)


class SomeUserEvent(UserEvent):
    name = "some_user_event"
    routing_key_fmt = "some.user.event"

    def __init__(self, a, b, tenant_uuid, user_uuid) -> None:
        content = {"a": a, "b": b}
        super().__init__(content, tenant_uuid, user_uuid)


class SomeMultiUserEvent(MultiUserEvent):
    name = "some_multi_user_event"
    routing_key_fmt = "some.multi.user.event"

    def __init__(self, a, b, tenant_uuid, user_uuids) -> None:
        content = {"a": a, "b": b}
        super().__init__(content, tenant_uuid, user_uuids)


def test_service_event_headers():
    event = SomeServiceEvent(1, 2)
    assert event.headers == {"name": "some_service_event"}


def test_service_event_marshal():
    event = SomeServiceEvent(1, 2)
    assert event.marshal() == {"a": 1, "b": 2}


def test_tenant_event_headers():
    event = SomeTenantEvent(1, 2, TENANT_UUID)
    assert event.headers == {
        "name": "some_tenant_event",
        "user_uuid:*": True,  # Corrected assertion
        "tenant_uuid": TENANT_UUID,
    }


def test_tenant_event_marshal():
    event = SomeTenantEvent(1, 2, TENANT_UUID)
    assert event.marshal() == {"a": 1, "b": 2}


def test_tenant_event_no_tenant():
    with pytest.raises(ValueError, match="tenant_uuid must have a value"):
        SomeTenantEvent(1, 2, None)


def test_user_event_headers():
    event = SomeUserEvent(1, 2, TENANT_UUID, USER_UUID)
    assert event.headers == {
        "name": "some_user_event",
        "tenant_uuid": TENANT_UUID,
        f"user_uuid:{USER_UUID}": True,  # using f-string
    }


def test_user_event_marshal():
    event = SomeUserEvent(1, 2, TENANT_UUID, USER_UUID)
    assert event.marshal() == {"a": 1, "b": 2}


def test_multi_user_event_headers():
    event = SomeMultiUserEvent(5, 6, TENANT_UUID, [USER_UUID, USER2_UUID, USER3_UUID])
    assert event.headers == {
        "name": "some_multi_user_event",
        "tenant_uuid": TENANT_UUID,
        f"user_uuid:{USER_UUID}": True,  # using f-string
        f"user_uuid:{USER2_UUID}": True,  # using f-string
        f"user_uuid:{USER3_UUID}": True,  # using f-string
    }


def test_multi_user_event_marshal():
    event = SomeMultiUserEvent(5, 6, TENANT_UUID, [USER_UUID, USER2_UUID, USER3_UUID])
    assert event.marshal() == {"a": 5, "b": 6}


def test_multi_user_event_not_list():
    with pytest.raises(ValueError, match="user_uuids must be a list of uuids"):
        SomeMultiUserEvent(5, 6, TENANT_UUID, USER_UUID)  # not a list.
