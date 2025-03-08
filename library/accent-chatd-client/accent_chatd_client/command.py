# Copyright 2023 Accent Communications

from accent_lib_rest_client.command import RESTCommand

from .exceptions import ChatdError, ChatdServiceUnavailable, InvalidChatdError


class ChatdCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise ChatdServiceUnavailable(response)

        try:
            raise ChatdError(response)
        except InvalidChatdError:
            RESTCommand.raise_from_response(response)
