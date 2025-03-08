# Copyright 2023 Accent Communications


class PJSIPDocService:
    def __init__(self, confd_client):
        self._confd = confd_client
        self._cached_doc = None

    def get(self):
        if self._cached_doc is None:
            self._cached_doc = self._confd.pjsip_doc.get()

        return self._cached_doc


class PJSIPGlobalSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.pjsip_global.get()

    def update(self, pjsip_global):
        self._confd.pjsip_global.update(pjsip_global)


class PJSIPSystemSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.pjsip_system.get()

    def update(self, pjsip_system):
        self._confd.pjsip_system.update(pjsip_system)


class IaxGeneralSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.iax_general.get(),
            'callnumberlimits': self._confd.iax_callnumberlimits.get()['items'],
        }
        return resource

    def update(self, resource):
        self._confd.iax_callnumberlimits.update({'items': resource['callnumberlimits']})
        resource['general']['ordered_options'] = self._confd.iax_general.get()[
            'ordered_options'
        ]
        self._confd.iax_general.update(resource['general'])


class SCCPDocService:
    def get(self):
        return [
            {'id': 'cid_name', 'text': 'cid_name'},
            {'id': 'cid_num', 'text': 'cid_num'},
            {'id': 'allow', 'text': 'allow'},
            {'id': 'disallow', 'text': 'disallow'},
        ]


class SCCPGeneralSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.sccp_general.get()

    def update(self, sccp_general):
        self._confd.sccp_general.update(sccp_general)


class VoicemailGeneralSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.voicemail_general.get(),
            'zonemessages': self._confd.voicemail_zonemessages.get()['items'],
        }
        return resource

    def update(self, resource):
        self._confd.voicemail_zonemessages.update({'items': resource['zonemessages']})
        self._confd.voicemail_general.update(resource['general'])


class TimezoneService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def list_timezones(self):
        return self._confd.timezones.list()


class FeaturesGeneralSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.features_general.get(),
            'featuremap': self._confd.features_featuremap.get(),
            'applicationmap': self._confd.features_applicationmap.get(),
        }
        return resource

    def update(self, resource):
        self._confd.features_featuremap.update(resource['featuremap'])
        self._confd.features_applicationmap.update(resource['applicationmap'])
        self._confd.features_general.update(resource['general'])


class ConfBridgeGeneralSettingsService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'accent_default_user': self._confd.confbridge_accent_default_user.get(),
            'accent_default_bridge': self._confd.confbridge_accent_default_bridge.get(),
        }
        return resource

    def update(self, resource):
        self._confd.confbridge_accent_default_user.update(resource['accent_default_user'])
        self._confd.confbridge_accent_default_bridge.update(
            resource['accent_default_bridge']
        )
