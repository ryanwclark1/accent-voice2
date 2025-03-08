# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl, required_master_tenant
from accent_confd.helpers.asterisk import AsteriskConfigurationList


class ConfBridgeAccentDefaultBridgeList(AsteriskConfigurationList):
    section_name = 'accent_default_bridge'

    @required_master_tenant()
    @required_acl('confd.asterisk.confbridge.accent_default_bridge.get')
    def get(self):
        return super().get()

    @required_master_tenant()
    @required_acl('confd.asterisk.confbridge.accent_default_bridge.update')
    def put(self):
        return super().put()


class ConfBridgeAccentDefaultUserList(AsteriskConfigurationList):
    section_name = 'accent_default_user'

    @required_master_tenant()
    @required_acl('confd.asterisk.confbridge.accent_default_user.get')
    def get(self):
        return super().get()

    @required_master_tenant()
    @required_acl('confd.asterisk.confbridge.accent_default_user.update')
    def put(self):
        return super().put()
