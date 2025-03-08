# Copyright 2023 Accent Communications

import logging

from accent.asterisk.protocol_interface import protocol_interface_from_channel
from ari.exceptions import ARINotFound

from accent_calld.plugins.dial_mobile.services import DialMobileService

logger = logging.getLogger(__name__)


class EventHandler:
    def __init__(self, service):
        self._service: DialMobileService = service

    def subscribe(self, bus_consumer):
        bus_consumer.subscribe('BridgeEnter', self._on_bridge_enter)
        bus_consumer.subscribe('DialEnd', self._on_dial_end)
        bus_consumer.subscribe('UserEvent', self._on_user_event)
        bus_consumer.subscribe(
            'auth_refresh_token_created', self._on_refresh_token_created
        )
        bus_consumer.subscribe(
            'auth_refresh_token_deleted', self._on_refresh_token_deleted
        )

    def _on_user_event(self, event):
        if event['UserEvent'] != 'Pushmobile':
            return

        user_uuid = event['ACCENT_DST_UUID']
        video_enabled = event['ACCENT_VIDEO_ENABLED'] == '1'
        ring_timeout = event['ACCENT_RING_TIME']
        tenant_uuid = event.get('ChanVariable', {}).get('ACCENT_TENANT_UUID')
        timestamp = event['ACCENT_TIMESTAMP']

        logger.info(
            'Received push notification request for user %s from %s <%s>',
            user_uuid,
            event["CallerIDName"],
            event["CallerIDNum"],
        )

        self._service.send_push_notification(
            tenant_uuid,
            user_uuid,
            event["Uniqueid"],
            event['ChanVariable']['ACCENT_SIP_CALL_ID'],
            event["CallerIDName"],
            event["CallerIDNum"],
            video_enabled,
            ring_timeout,
            event["Linkedid"],
            timestamp,
        )

    def _on_refresh_token_created(self, event):
        if not event['mobile']:
            return

        self._service.on_mobile_refresh_token_created(event['user_uuid'])

    def _on_refresh_token_deleted(self, event):
        if not event['mobile']:
            return

        self._service.on_mobile_refresh_token_deleted(event['user_uuid'])

    def _on_bridge_enter(self, event):
        if not event['BridgeUniqueid'].startswith('accent-dial-mobile-'):
            return

        protocol, endpoint = protocol_interface_from_channel(event['Channel'])
        if protocol.lower() != 'sip':
            return

        linkedid = event['Linkedid']
        user_uuid = event['ChanVariable']['ACCENT_USERUUID']

        try:
            has_a_registered_mobile_and_pending_push = (
                self._service.has_a_registered_mobile_and_pending_push(
                    linkedid,
                    event['Uniqueid'],
                    endpoint,
                    user_uuid,
                )
            )
        except ARINotFound:
            # The channel that entered the bridge has already been hung up
            return self._service.cancel_push_mobile(linkedid)

        if has_a_registered_mobile_and_pending_push:
            self._service.remove_pending_push_mobile(linkedid)
        else:
            self._service.cancel_push_mobile(linkedid)

    def _on_dial_end(self, event):
        # Ignore dial_end if it's in an unrelated context
        if event['DestContext'] != 'accent_wait_for_registration':
            return

        # Ignore dial_end if the call was answered, those are handled in _on_bridge_enter
        if event['DialStatus'] == 'ANSWER':
            return

        self._service.cancel_push_mobile(event['Uniqueid'])
