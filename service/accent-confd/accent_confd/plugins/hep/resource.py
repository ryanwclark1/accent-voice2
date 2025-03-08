# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl, required_master_tenant
from accent_confd.helpers.asterisk import AsteriskConfigurationList


class HEPGeneralList(AsteriskConfigurationList):
    section_name = 'general'

    @required_master_tenant()
    @required_acl('confd.asterisk.hep.general.get')
    def get(self):
        return super().get()

    @required_master_tenant()
    @required_acl('confd.asterisk.hep.general.update')
    def put(self):
        return super().put()
