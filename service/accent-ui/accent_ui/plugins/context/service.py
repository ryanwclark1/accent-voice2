# Copyright 2023 Accent Communications

from accent_ui.helpers.service import BaseConfdService


class ContextService(BaseConfdService):
    resource_confd = 'contexts'

    def __init__(self, confd_client):
        self._confd = confd_client

    # NOTE: temporary fix for the non-usage of the UUID by the API
    def list(self, *args, **kwargs):
        results = super().list(*args, **kwargs)
        for context in results['items']:
            del context['uuid']
        return results

    def update(self, context):
        super().update(context)
        included_contexts = [
            {'id': context_id} for context_id in context['context_ids']
        ]
        self._confd.contexts(context['id']).update_contexts(included_contexts)
