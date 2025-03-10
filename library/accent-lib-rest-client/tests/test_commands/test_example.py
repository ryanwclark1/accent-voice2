import pytest

from accent_lib_rest_client.example_cmd import ExampleCommand

from ..command_base import RESTCommandBase


class TestExampleCommand(RESTCommandBase):
    class Command(ExampleCommand):
        pass

    def test_test_method(self, mocker):
        """Test the example test method."""
        expected_response = {'foo': 'bar'}
        self.set_response(mocker, 'get', 200, expected_response)

        result = self.command.test()

        assert result == b'{"foo": "bar"}'
        self.assert_request_sent('get', self.base_url)

    def test_test_method_error(self, mocker):
        """Test error handling in test method."""
        self.set_response(mocker, 'get', 404)

        with pytest.raises(HTTPError):
            self.command.test()

    @pytest.mark.parametrize('status_code,expected_error', [
        (400, HTTPError),
        (401, HTTPError),
        (403, HTTPError),
        (500, HTTPError),
        (503, HTTPError)
    ])
    def test_error_status_codes(self, mocker, status_code, expected_error):
        """Test various error status codes."""
        self.set_response(mocker, 'get', status_code)

        with pytest.raises(expected_error):
            self.command.test()

    def test_custom_headers(self, mocker):
        """Test request with custom headers."""
        headers = {'Custom-Header': 'test-value'}
        self.set_response(mocker, 'get', 200, {'foo': 'bar'})

        self.command.test(headers=headers)

        self.assert_request_sent('get', self.base_url, headers=headers)

    @pytest.mark.asyncio
    async def test_async_execution(self, mocker):
        """Test async execution if supported."""
        self.set_response(mocker, 'get', 200, {'foo': 'bar'})

        result = await self.command.test()

        assert result == b'{"foo": "bar"}'


    def test_get_data(self, mocker):
        self.set_response(mocker, 'get', 200, {'data': 'test'})
        result = self.command.get_data()
        assert result == {'data': 'test'}
        self.assert_request_sent('get', f'{self.base_url}/data')