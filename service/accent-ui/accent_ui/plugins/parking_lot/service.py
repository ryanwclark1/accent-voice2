# Copyright 2023 Accent Communications

from accent_ui.helpers.extension import BaseConfdExtensionService


class ParkingLotService(BaseConfdExtensionService):
    resource_confd = 'parking_lots'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_music_on_hold(self, name):
        results = self._confd.moh.list(name=name)
        for result in results['items']:
            return result
