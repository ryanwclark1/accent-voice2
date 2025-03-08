# Copyright 2023 Accent Communications

from accent_lib_rest_client.client import BaseClient


class Client(BaseClient):
    namespace = 'accent_market_client.commands'

    def __init__(
        self, host='apps.accentvoice.io', port=None, version='v1', https=False, **kwargs
    ):
        super().__init__(host=host, port=port, version=version, https=https, **kwargs)
