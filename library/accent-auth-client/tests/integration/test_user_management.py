# Copyright 2025 Accent Communications

import pytest
import httpx
from unittest.mock import patch, MagicMock

from accent_auth_client import Client


@pytest.mark.integration
class TestUserManagement:
    """Integration tests for user management operations."""

    @pytest.fixture
    def client(self):
        """Create a client instance with mocked responses for user operations."""
        client = Client(
            host="test.example.com", port=443, version="0.1", token="test-admin-token"
        )

        # Override sync client for test
        client._sync_client = MagicMock(spec=httpx.Client)

        # Configure responses for different user endpoints
        def get_response_for_request(*args, **kwargs):
            url = args[0]
            method = kwargs.get("_request_method", "GET")

            response = MagicMock(spec=httpx.Response)

            # User creation
            if url.endswith("/users") and method == "POST":
                response.status_code = 200
                response.json.return_value = {
                    "uuid": "00000000-0000-4000-a000-000000000001",
                    "username": kwargs.get("json", {}).get("username", "newuser"),
                    "firstname": kwargs.get("json", {}).get("firstname", ""),
                    "lastname": kwargs.get("json", {}).get("lastname", ""),
                    "emails": [
                        {
                            "uuid": "00000000-0000-4000-a000-000000000010",
                            "address": kwargs.get("json", {}).get(
                                "email", "test@example.com"
                            ),
                            "confirmed": False,
                            "main": True,
                        }
                    ],
                }

            # User listing
            elif url.endswith("/users") and method == "GET":
                response.status_code = 200
                response.json.return_value = {
                    "items": [
                        {
                            "uuid": "00000000-0000-4000-a000-000000000001",
                            "username": "testuser",
                        }
                    ],
                    "total": 1,
                }

            # Get user
            elif "/users/" in url and method == "GET" and not url.endswith("/emails"):
                user_uuid = url.split("/users/")[1].split("/")[0]
                response.status_code = 200
                response.json.return_value = {
                    "uuid": user_uuid,
                    "username": "testuser",
                    "firstname": "Test",
                    "lastname": "User",
                    "emails": [
                        {
                            "uuid": "00000000-0000-4000-a000-000000000010",
                            "address": "test@example.com",
                            "confirmed": True,
                            "main": True,
                        }
                    ],
                }

            # Update user emails
            elif "/users/" in url and url.endswith("/emails") and method == "PUT":
                response.status_code = 200
                emails = kwargs.get("json", {}).get("emails", [])
                email_objects = []
                for email in emails:
                    email_objects.append(
                        {
                            "uuid": "00000000-0000-4000-a000-000000000010",
                            "address": email,
                            "confirmed": False,
                            "main": True,
                        }
                    )

                response.json.return_value = {"emails": email_objects}

            # Delete user
            elif "/users/" in url and method == "DELETE":
                response.status_code = 204

            # Default response
            else:
                response.status_code = 404
                response.json.return_value = {"message": "Not found"}

            return response

        # Set up mock methods with custom responses
        def mock_get(url, **kwargs):
            kwargs["_request_method"] = "GET"
            return get_response_for_request(url, **kwargs)

        def mock_post(url, **kwargs):
            kwargs["_request_method"] = "POST"
            return get_response_for_request(url, **kwargs)

        def mock_put(url, **kwargs):
            kwargs["_request_method"] = "PUT"
            return get_response_for_request(url, **kwargs)

        def mock_delete(url, **kwargs):
            kwargs["_request_method"] = "DELETE"
            return get_response_for_request(url, **kwargs)

        client._sync_client.get = mock_get
        client._sync_client.post = mock_post
        client._sync_client.put = mock_put
        client._sync_client.delete = mock_delete

        return client

    def test_user_crud_operations(self, client):
        """Test Create, Read, Update, and Delete operations on users."""
        # Step 1: Create a new user
        new_user = client.users.new(
            username="newuser",
            firstname="New",
            lastname="User",
            email="new@example.com",
        )

        assert new_user["uuid"] == "00000000-0000-4000-a000-000000000001"
        assert new_user["username"] == "newuser"
        assert new_user["emails"][0]["address"] == "new@example.com"

        # Step 2: Get the user
        user = client.users.get(new_user["uuid"])

        assert user["uuid"] == new_user["uuid"]
        assert user["username"] == "testuser"  # This comes from our mocked response

        # Step 3: List users
        users = client.users.list()

        assert users["total"] == 1
        assert users["items"][0]["uuid"] == "00000000-0000-4000-a000-000000000001"

        # Step 4: Update user emails
        updated_emails = client.users.update_emails(
            user["uuid"], ["updated@example.com", "second@example.com"]
        )

        assert len(updated_emails["emails"]) == 2
        assert updated_emails["emails"][0]["address"] == "updated@example.com"
        assert updated_emails["emails"][1]["address"] == "second@example.com"

        # Step 5: Delete the user
        client.users.delete(user["uuid"])

        # No assertion needed since we're just checking that the call doesn't raise an exception
