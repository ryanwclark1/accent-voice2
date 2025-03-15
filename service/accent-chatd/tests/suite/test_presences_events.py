# integration_tests/suite/test_presences_events.py
import uuid

import pytest
from accent_test_helpers import generate_uuid
from hamcrest import assert_that, equal_to, has_properties

from accent_chatd.models import User

from .helpers.base import APIIntegrationTest, use_asset


@use_asset("base")
class TestPresenceEvents(APIIntegrationTest):
    def test_user_created_event(self):
        user_uuid = str(generate_uuid())
        tenant_uuid = str(generate_uuid())
        # Publish the event using the helper function on bus
        self.bus.publish(
            message={"uuid": user_uuid, "tenant_uuid": tenant_uuid},
            routing_key="",
            headers={"name": "user_created", "tenant_uuid": tenant_uuid},
        )

        # Check if the user was created in the database
        user = self._session.query(User).filter_by(uuid=user_uuid).first()
        assert user is not None
        assert str(user.tenant_uuid) == tenant_uuid
        assert user.state == "unavailable"

    def test_user_deleted_event(self):
        user_uuid = str(generate_uuid())
        tenant_uuid = str(generate_uuid())
        # Create the user first, so we have one to delete
        self.bus.publish(
            message={"uuid": user_uuid, "tenant_uuid": tenant_uuid},
            routing_key="",
            headers={"name": "user_created", "tenant_uuid": tenant_uuid},
        )
        # Publish delete event.
        self.bus.publish(
            message={"uuid": user_uuid, "tenant_uuid": tenant_uuid},
            routing_key="",
            headers={"name": "user_deleted", "tenant_uuid": tenant_uuid},
        )

        user = self._session.query(User).filter_by(uuid=user_uuid).first()
        assert user is None
