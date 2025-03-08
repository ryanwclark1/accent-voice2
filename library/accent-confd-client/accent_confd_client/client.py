# Copyright 2023 Accent Communications

from accent_lib_rest_client.client import BaseClient

from accent_confd_client.session import ConfdSession


class ConfdClient(BaseClient):
    namespace = 'accent_confd_client.commands'

    def __init__(self, host, port=443, prefix='/api/confd', version='1.1', **kwargs):
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)

    def session(self):
        session = super().session()
        return ConfdSession(session, self.url())
