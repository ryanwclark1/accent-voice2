# Copyright 2023 Accent Communications

from accent_lib_rest_client.client import BaseClient


class DeploydClient(BaseClient):
    namespace = 'accent_deployd_client.commands'

    def __init__(self, host, port=443, prefix='/api/deployd', version='0.1', **kwargs):
        super().__init__(
            host=host,
            port=port,
            prefix=prefix,
            version=version,
            **kwargs,
        )
