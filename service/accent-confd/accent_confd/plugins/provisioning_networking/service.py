# Copyright 2023 Accent Communications

from accent_confd.database import provisioning_networking as provisioning_networking_dao


class ProvisioningNetworkingService:
    def __init__(self, notifier, sysconfd):
        self.notifier = notifier
        self.sysconfd = sysconfd

    def get(self):
        return provisioning_networking_dao.get()

    def edit(self, resource):
        provisioning_networking_dao.update(resource)
        self.notifier.edited(resource)
