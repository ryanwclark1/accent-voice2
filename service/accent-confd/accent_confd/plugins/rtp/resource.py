# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl, required_master_tenant
from accent_confd.helpers.asterisk import AsteriskConfigurationList


class RTPGeneralList(AsteriskConfigurationList):
    section_name = 'general'

    @required_master_tenant()
    @required_acl('confd.asterisk.rtp.general.get')
    def get(self):
        return super().get()

    @required_master_tenant()
    @required_acl('confd.asterisk.rtp.general.update')
    def put(self):
        return super().put()


class RTPIceHostCandidatesList(AsteriskConfigurationList):
    section_name = 'ice_host_candidates'

    @required_master_tenant()
    @required_acl('confd.asterisk.rtp.ice_host_candidates.get')
    def get(self):
        return super().get()

    @required_master_tenant()
    @required_acl('confd.asterisk.rtp.ice_host_candidates.update')
    def put(self):
        return super().put()
