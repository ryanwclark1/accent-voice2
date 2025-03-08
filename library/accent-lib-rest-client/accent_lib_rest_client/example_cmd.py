# Copyright 2024 Accent Communications

from accent_lib_rest_client.command import RESTCommand


class ExampleCommand(RESTCommand):
    """Example REST command implementation."""

    resource = 'test'

    def __call__(self) -> bytes:
        """Execute the test command."""
        return self.test()

    def test(self) -> bytes:
        """Perform test request."""
        response = self.get(response_model=None)
        return response.content
