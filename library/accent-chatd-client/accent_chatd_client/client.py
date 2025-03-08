# Copyright 2023 Accent Communications

from accent_lib_rest_client.client import BaseClient


class ChatdClient(BaseClient):
    namespace = 'accent_chatd_client.commands'

    def __init__(self, host, port=443, prefix='/api/chatd', version='1.0', **kwargs):
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
