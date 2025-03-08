# Copyright 2023 Accent Communications

from accent_confd_client.crud import CRUDCommand


class ExtensionsFeaturesCommand(CRUDCommand):
    resource = 'extensions/features'

    def create(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()
