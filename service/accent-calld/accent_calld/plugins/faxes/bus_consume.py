# Copyright 2023 Accent Communications

import logging

from .schemas import fax_schema

logger = logging.getLogger(__name__)


class FaxesBusEventHandler:
    def __init__(self, notifier):
        self._notifier = notifier

    def subscribe(self, bus_consumer):
        bus_consumer.subscribe('UserEvent', self._fax_result)

    def _fax_result(self, event):
        if event['UserEvent'] != 'FaxProgress':
            return

        fax_infos = {
            'context': event['ACCENT_FAX_DESTINATION_CONTEXT'],
            'extension': event['ACCENT_FAX_DESTINATION_EXTENSION'],
            'caller_id': event['ACCENT_FAX_CALLER_ID'],
            'call_id': event['Uniqueid'],
            'id': event['Uniqueid'],
            'user_uuid': event['ACCENT_USERUUID'] or None,
            'tenant_uuid': event['ACCENT_TENANT_UUID'] or None,
        }
        fax = fax_schema.dump(fax_infos)
        if event['STATUS'] == 'SUCCESS':
            self._notifier.notify_fax_succeeded(fax)
        elif event['STATUS'] == 'FAILED':
            fax['error'] = event['ERROR']
            self._notifier.notify_fax_failed(fax)
