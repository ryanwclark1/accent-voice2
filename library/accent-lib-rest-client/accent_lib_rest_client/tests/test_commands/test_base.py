import pytest
from pydantic import BaseModel

from accent_lib_rest_client.command import RESTCommand
from accent_lib_rest_client.exceptions import HTTPError, ResponseValidationError

from ..command_base import RESTCommandBase


class TestModel(BaseModel):
    message: str

class TestBaseCommand(RESTCommandBase):
    class Command(RESTCommand):
        resource = 'test'

    def test_initialization(self):
        """Test command initialization."""
        assert self.command._client == self.client
        assert self.command.base_url == self.base_url
        assert self.command.timeout == self.client.timeout

    @pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete'])
    def test_http_methods(self, mocker, method):
        """Test all HTTP methods."""
        response_data = {'message': 'test'}
        self.set_response(mocker, method, 200, response_data)

        cmd_method = getattr(self.command, method)
        result = cmd_method(response_model=TestModel)

        assert isinstance(result, TestModel)
        assert result.message == 'test'
        self.assert_request_sent(method, self.base_url)

    def test_error_response(self, mocker):
        """Test error response handling."""
        self.set_response(mocker, 'get', 404, {'message': 'Not Found'})

        with pytest.raises(HTTPError):
            self.command.get()

    def test_validation_error(self, mocker):
        """Test validation error handling."""
        invalid_data = {'wrong_field': 'value'}
        self.set_response(mocker, 'get', 200, invalid_data)

        with pytest.raises(ResponseValidationError):
            self.command.get(response_model=TestModel)