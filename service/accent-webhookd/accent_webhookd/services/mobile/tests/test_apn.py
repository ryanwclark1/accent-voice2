# Copyright 2023 Accent Communications

from typing import Any
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to

from accent_webhookd.services.mobile.plugin import (
    NotificationPayload,
    NotificationType,
    PushNotification,
)


class TestAPN(TestCase):
    def setUp(self):
        self.task = Mock()
        self.config = {
            'mobile_apns_host': 'api.push.apple.com',
            'mobile_apns_port': 443,
            'mobile_apns_call_topic': 'org.accentvoice.voip',
            'mobile_apns_default_topic': 'org.accentvoice',
        }
        self.external_tokens = {
            'apns_voip_token': s.apns_voip_token,
            'apns_notification_token': s.apns_notification_token,
        }
        self.external_config: dict[str, Any] = {}
        self.jwt = ''
        self._push = PushNotification(
            self.task,
            self.config,  # type: ignore
            self.external_tokens,  # type: ignore
            self.external_config,  # type: ignore
            self.jwt,
        )

    def test_accent_notification_call(self):
        message_title = None
        message_body = None
        data: NotificationPayload = {
            'notification_type': NotificationType.INCOMING_CALL,
            'items': {},
        }

        headers, payload, token = self._push._create_apn_message(
            message_title,
            message_body,
            data,
        )

        assert_that(
            headers,
            equal_to(
                {
                    'apns-topic': 'org.accentvoice.voip',
                    'apns-push-type': 'voip',
                    'apns-priority': '10',
                }
            ),
        )
        assert_that(
            payload,
            equal_to(
                {
                    'aps': {'alert': data, 'badge': 1},
                    'notification_type': NotificationType.INCOMING_CALL,
                    'items': {},
                }
            ),
        )
        assert_that(token, equal_to(s.apns_voip_token))

    def test_accent_cancel_notification(self):
        message_title = None
        message_body = None
        data: NotificationPayload = {
            'notification_type': NotificationType.CANCEL_INCOMING_CALL,
            'items': {},
        }

        headers, payload, token = self._push._create_apn_message(
            message_title,
            message_body,
            data,
        )

        assert_that(
            headers,
            equal_to(
                {
                    'apns-topic': 'org.accentvoice',
                    'apns-push-type': 'alert',
                    'apns-priority': '5',
                }
            ),
        )
        assert_that(
            payload,
            equal_to(
                {
                    'aps': {"badge": 1, "sound": "default", "content-available": 1},
                    'notification_type': NotificationType.CANCEL_INCOMING_CALL,
                    'items': {},
                }
            ),
        )
        assert_that(token, equal_to(s.apns_notification_token))
