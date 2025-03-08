# Copyright 2023 Accent Communications

from accent_ui.helpers.extension import BaseConfdExtensionService


class ConferenceService(BaseConfdExtensionService):
    resource_confd = 'conferences'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_first_internal_context(self):
        result = self._confd.contexts.list(
            type='internal', limit=1, direction='asc', order='id'
        )
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_music_on_hold(self, name):
        results = self._confd.moh.list(name=name)
        for result in results['items']:
            return result
