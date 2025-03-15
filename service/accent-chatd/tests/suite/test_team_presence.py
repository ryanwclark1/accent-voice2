# integration_tests/suite/test_teams_presence.py

import uuid
from datetime import UTC, datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest
from accent_test_helpers import generate_uuid

from .helpers.base import TeamsAssetLaunchingTestCase, use_asset


@use_asset("teams")
class TestTeamsPresence(TeamsAssetLaunchingTestCase):
    def setUp(self):
        super().setUp()
        self.user_uuid = str(generate_uuid())
        self.teams_user_id = "test_teams_user_id"
        self.token = "dummy_token"  # Placeholder token
        self.url = f"/1.0/users/{self.user_uuid}/teams/presence"

    @pytest.fixture
    def mock_service(self):
        with patch(
            "accent_chatd.api.teams_presence.routes.get_teams_service",
            new_callable=AsyncMock,
        ) as mock:
            yield mock

    async def test_update_teams_presence_validation_token(self, mock_service):
        """Test handling of the validationToken."""
        validation_token = "test_validation_token"

        # Use the mock service
        mock_service.return_value.is_connected.return_value = True
        # aiohttp uses query and body
        response = self.chatd.http_client.post(
            self.url, params={"validationToken": validation_token}
        )
        assert response.status_code == 200
        assert response.content.decode() == validation_token  # Should return the token
        assert response.headers["Content-Type"] == "text/plain"

    async def test_update_teams_presence_user_not_connected(self, mock_service):
        """Test that disconnected users return 404."""
        mock_service.return_value.is_connected.return_value = False

        response = self.chatd.http_client.post(self.url, json={})  # Empty JSON payload
        assert response.status_code == 404

    async def test_update_teams_presence_receives_update(self, mock_service):
      """Test that presence updates are received and processed."""
      mock_service.return_value.is_connected.return_value = True
      mock_service.return_value.fetch_teams_presence.return_value = {
          "availability": "Busy"
      }
      # Simulate a presence update from MS Graph
      update_payload = {
          'value': [
              {
                  'subscriptionId': str(uuid.uuid4()),
                  'subscriptionExpirationDateTime': (
                      datetime.now(timezone.utc) + timedelta(minutes=30)
                  ).isoformat(),
                  'changeType': 'updated',
                  'resource': f'/communications/presences/test_user_id',
                  'resourceData': {'id': 'test_user_id', 'availability': 'Busy'},
                  'clientState': 'test_state'
              }
          ]
      }
      response = self.chatd.http_client.post(
          self.url, json=update_payload
      )
      assert response.status_code == 200
      # Assert service methods were called.
      mock_service.return_value.fetch_teams_presence.assert_called_with("test_user_id", "dummy_token") # Updated
      mock_service.return_value.update_presence.assert_called_with("Busy", self.user_uuid)

    async def test_update_teams_presence_invalid_payload(self, mock_service):
        """Test handling invalid presence update payloads"""
        mock_service.return_value.is_connected.return_value = True
        # Invalid, changeType is missing
        invalid_payload = {
            "value": [
                {
                    "subscriptionId": str(uuid.uuid4()),
                    "subscriptionExpirationDateTime": (
                        datetime.now(UTC) + timedelta(minutes=30)
                    ).isoformat(),
                    "resource": "/communications/presences/test_user_id",
                    "resourceData": {
                        "id": "test_user_id",
                        "availability": "Busy",
                    },
                }
            ]
        }
        response = self.chatd.http_client.post(self.url, json=invalid_payload)
        assert response.status_code == 422  # Unprocessable
