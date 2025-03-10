# Copyright 2025 Accent Communications

"""Mock server implementations for testing.

This module provides mock servers that can be used for integration testing.
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional, Tuple, Callable
from urllib.parse import parse_qs, urlparse

from .responses import (
    create_token_response,
    create_user_response,
    create_users_list_response,
    create_group_response,
    create_policy_response,
    create_error_response,
)


class MockAPIHandler(BaseHTTPRequestHandler):
    """Mock HTTP request handler for testing."""

    # Class-level storage for route handlers
    routes: Dict[Tuple[str, str], Callable] = {}

    # Authentication tokens
    valid_tokens = ["test-token-12345"]

    def do_GET(self):
        """Handle GET requests."""
        self._handle_request("GET")

    def do_POST(self):
        """Handle POST requests."""
        self._handle_request("POST")

    def do_PUT(self):
        """Handle PUT requests."""
        self._handle_request("PUT")

    def do_DELETE(self):
        """Handle DELETE requests."""
        self._handle_request("DELETE")

    def do_HEAD(self):
        """Handle HEAD requests."""
        self._handle_request("HEAD")

    def do_PATCH(self):
        """Handle PATCH requests."""
        self._handle_request("PATCH")

    def _parse_body(self):
        """Parse the request body as JSON."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode("utf-8"))
        return {}

    def _handle_request(self, method):
        """Handle request based on method and path."""
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # Get auth token from headers
        auth_token = self.headers.get("X-Auth-Token")

        # Check if this is a token check
        if method == "HEAD" and path.startswith("/api/auth/0.1/token/"):
            token = path.split("/token/")[1]
            if token in self.valid_tokens:
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
            return

        # For other endpoints, check auth unless it's the token creation endpoint
        if not path.endswith("/token") and auth_token not in self.valid_tokens:
            self._send_json_response(
                401, create_error_response(401, "Authentication required")
            )
            return

        # Look for a route handler
        handler = self.routes.get((method, path))
        if handler:
            body = self._parse_body() if method in ("POST", "PUT", "PATCH") else {}
            handler(self, query, body, auth_token)
        else:
            self._send_json_response(
                404, create_error_response(404, f"No handler for {method} {path}")
            )

    def _send_json_response(self, status_code, data):
        """Send a JSON response with the given status code and data."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if data is not None:
            response = json.dumps(data).encode("utf-8")
            self.wfile.write(response)

    def _send_empty_response(self, status_code):
        """Send an empty response with the given status code."""
        self.send_response(status_code)
        self.end_headers()

    @classmethod
    def register_route(cls, method, path, handler):
        """Register a route handler.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path
            handler: Function to handle the request
        """
        cls.routes[(method, path)] = handler


class MockAuthServer:
    """Mock auth server for testing."""

    def __init__(self, host="localhost", port=8080):
        """Initialize the mock server.

        Args:
            host: Server hostname
            port: Server port
        """
        self.host = host
        self.port = port
        self.server = HTTPServer((host, port), MockAPIHandler)
        self.server_thread = None

        # Register default route handlers
        self._register_default_routes()

    def _register_default_routes(self):
        """Register default route handlers."""
        # Token creation
        MockAPIHandler.register_route(
            "POST", "/api/auth/0.1/token", self._handle_token_creation
        )

        # User operations
        MockAPIHandler.register_route(
            "GET", "/api/auth/0.1/users", self._handle_list_users
        )
        MockAPIHandler.register_route(
            "POST", "/api/auth/0.1/users", self._handle_create_user
        )
        MockAPIHandler.register_route(
            "GET",
            "/api/auth/0.1/users/00000000-0000-4000-a000-000000000001",
            self._handle_get_user,
        )

    def _handle_token_creation(self, handler, query, body, auth_token):
        """Handle token creation requests."""
        username = body.get("username", "testuser")
        token_response = create_token_response(
            token="test-token-12345", username=username
        )
        handler._send_json_response(200, token_response)

    def _handle_list_users(self, handler, query, body, auth_token):
        """Handle user listing requests."""
        users_response = create_users_list_response()
        handler._send_json_response(200, users_response)

    def _handle_create_user(self, handler, query, body, auth_token):
        """Handle user creation requests."""
        user_response = create_user_response(
            username=body.get("username", "newuser"),
            firstname=body.get("firstname", ""),
            lastname=body.get("lastname", ""),
            email=body.get("email", "test@example.com"),
        )
        handler._send_json_response(200, user_response)

    def _handle_get_user(self, handler, query, body, auth_token):
        """Handle get user requests."""
        user_response = create_user_response(
            user_uuid="00000000-0000-4000-a000-000000000001"
        )
        handler._send_json_response(200, user_response)

    def start(self):
        """Start the mock server in a background thread."""
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"Mock server running at http://{self.host}:{self.port}")

    def stop(self):
        """Stop the mock server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Mock server stopped")
