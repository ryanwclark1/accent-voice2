# Copyright 2023 Accent Communications

from requests import HTTPError, RequestException

from accent_calld.plugin_helpers.confd import not_found
from accent_calld.plugin_helpers.exceptions import AccentConfdUnreachable
from accent_calld.plugins.switchboards.exceptions import NoSuchSwitchboard


class Switchboard:
    def __init__(self, tenant_uuid, uuid, confd_client):
        self.tenant_uuid = tenant_uuid
        self.uuid = uuid
        self._confd = confd_client

    def exists(self):
        try:
            self._get()
        except NoSuchSwitchboard:
            return False
        else:
            return True

    def hold_moh(self):
        return self._get()['waiting_room_music_on_hold']

    def queue_moh(self):
        return self._get()['queue_music_on_hold']

    def _get(self):
        try:
            return self._confd.switchboards.get(self.uuid, tenant_uuid=self.tenant_uuid)
        except HTTPError as e:
            if not_found(e):
                raise NoSuchSwitchboard(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)
