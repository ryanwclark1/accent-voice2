# integration_tests/suite/test_presences_events.py
import uuid

import pytest
from accent_test_helpers import generate_uuid

from .helpers.base import APIIntegrationTest, use_asset


@use_asset("base")
class TestPresenceEvents(APIIntegrationTest):
    def test_user_created_event(self):
        user_uuid = generate_uuid()
        tenant_uuid = generate_uuid()

        self.bus.send_user_created_event(user_uuid, tenant_uuid)

        # Check if the user was created in the database
        user = self._session.query(User).filter_by(uuid=user_uuid).first()
        assert user is not None
        assert user.tenant_uuid == tenant_uuid
        assert user.state == "unavailable"

    def test_user_deleted_event(self):
        user_uuid = generate_uuid()
        tenant_uuid = generate_uuid()
        # Create the user first, so we have one to delete
        self.bus.send_user_created_event(user_uuid, tenant_uuid)

        self.bus.send_user_deleted_event(user_uuid, tenant_uuid)
        user = self._session.query(User).filter_by(uuid=user_uuid).first()
        assert user is None
