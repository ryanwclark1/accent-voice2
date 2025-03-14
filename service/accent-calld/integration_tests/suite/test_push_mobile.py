# Copyright 2023 Accent Communications

from accent_amid_client import Client as AmidClient
from accent_test_helpers import until
from accent_test_helpers.hamcrest.timestamp import an_iso_timestamp
from hamcrest import assert_that, contains_exactly, has_entries, has_item

from .helpers.constants import CALLD_SERVICE_TOKEN
from .helpers.real_asterisk import RealAsteriskIntegrationTest


class TestPushMobile(RealAsteriskIntegrationTest):
    asset = 'real_asterisk'

    def setUp(self):
        super().setUp()
        self.amid = AmidClient(
            '127.0.0.1',
            port=self.service_port(9491, 'amid'),
            https=False,
            prefix=None,
            token=CALLD_SERVICE_TOKEN,
        )

    def test_send_push_mobile(self):
        events = self.bus.accumulator(headers={'name': 'call_push_notification'})

        push_mobile_event = {
            'data': {
                'UserEvent': 'Pushmobile',
                'Uniqueid': '1560784195.313',
                'ChanVariable': {
                    'ACCENT_BASE_EXTEN': '8000',
                    'ACCENT_DEREFERENCED_USERUUID': '',
                    'ACCENT_USERUUID': 'eaa18a7f-3f49-419a-9abb-b445b8ba2e03',
                    'ACCENT_TENANT_UUID': 'some-tenant-uuid',
                    'ACCENT_SIP_CALL_ID': 'de9eb39fb7585796',
                },
                'CallerIDName': 'my name is 8001',
                'Event': 'UserEvent',
                'ACCENT_DST_UUID': 'fb27eb93-d21c-483f-8068-e685c90b07e1',
                'ACCENT_RING_TIME': '42',
                'ACCENT_VIDEO_ENABLED': '1',
                'ACCENT_TIMESTAMP': '2024-08-06T11:59:59.999+00:00',
                'ConnectedLineName': 'bob 8000',
                'Priority': '2',
                'ChannelStateDesc': 'Ring',
                'Language': 'en_US',
                'CallerIDNum': '8001',
                'Exten': 's',
                'ChannelState': '4',
                'Channel': 'PJSIP/cfy381cl-00000139',
                'Context': 'accent-user-mobile-notification',
                'Linkedid': '1560784195.313',
                'ConnectedLineNum': '8000',
                'Privilege': 'user,all',
                'AccountCode': '',
            }
        }

        self.bus.publish(
            push_mobile_event,
            headers={'name': 'UserEvent'},
        )

        def bus_events_received():
            assert_that(
                events.accumulate(with_headers=True),
                has_item(
                    has_entries(
                        message=has_entries(
                            name='call_push_notification',
                            data=has_entries(
                                peer_caller_id_number='8001',
                                peer_caller_id_name='my name is 8001',
                                call_id='1560784195.313',
                                video=True,
                                sip_call_id='de9eb39fb7585796',
                                ring_timeout='42',
                                mobile_wakeup_timestamp=an_iso_timestamp(),
                            ),
                            required_acl='events.calls.fb27eb93-d21c-483f-8068-e685c90b07e1',
                        ),
                        headers=has_entries(
                            {
                                'name': 'call_push_notification',
                                'tenant_uuid': 'some-tenant-uuid',
                                'user_uuid:fb27eb93-d21c-483f-8068-e685c90b07e1': True,
                            }
                        ),
                    )
                ),
            )

        until.assert_(bus_events_received, timeout=10)

    def test_user_hint_is_updated_on_mobile_refresh_token(self):
        user_uuid = 'eaa18a7f-3f49-419a-9abb-b445b8ba2e03'
        tenant_uuid = 'some-tenant-uuid'
        client_id = 'calld-tests'

        self.bus.publish(
            {
                'name': 'auth_refresh_token_created',
                'data': {
                    'user_uuid': user_uuid,
                    'client_id': client_id,
                    'tenant_uuid': tenant_uuid,
                    'mobile': True,
                },
            },
            headers={
                'name': 'auth_refresh_token_created',
                'tenant_uuid': tenant_uuid,
                f'user_uuid:{user_uuid}': True,
            },
        )

        def user_hint_updated():
            result = self.amid.action(
                'Getvar', {'Variable': f'DEVICE_STATE(Custom:{user_uuid}-mobile)'}
            )
            assert_that(
                result,
                contains_exactly(
                    has_entries(
                        Response='Success',
                        Value='NOT_INUSE',
                    )
                ),
            )

        until.assert_(user_hint_updated, timeout=10)

        refresh_token = {'user_uuid': user_uuid, 'mobile': True}
        self.auth.set_refresh_tokens(refresh_token)

        self.bus.publish(
            {
                'name': 'auth_refresh_token_deleted',
                'data': {
                    'user_uuid': user_uuid,
                    'tenant_uuid': tenant_uuid,
                    'client_id': client_id,
                    'mobile': True,
                },
            },
            headers={
                'name': 'auth_refresh_token_deleted',
                'tenant_uuid': tenant_uuid,
                f'user_uuid:{user_uuid}': True,
            },
        )

        def user_hint_updated():  # type: ignore
            result = self.amid.action(
                'Getvar', {'Variable': f'DEVICE_STATE(Custom:{user_uuid}-mobile)'}
            )
            assert_that(
                result,
                contains_exactly(
                    has_entries(
                        Response='Success',
                        Value='NOT_INUSE',
                    )
                ),
            )

        until.assert_(user_hint_updated, timeout=10)

        self.auth.set_refresh_tokens()

        self.bus.publish(
            {
                'name': 'auth_refresh_token_deleted',
                'data': {
                    'user_uuid': user_uuid,
                    'tenant_uuid': tenant_uuid,
                    'client_id': client_id,
                    'mobile': True,
                },
            },
            headers={
                'name': 'auth_refresh_token_deleted',
                'tenant_uuid': tenant_uuid,
                f'user_uuid:{user_uuid}': True,
            },
        )

        def user_hint_updated():  # type: ignore
            result = self.amid.action(
                'Getvar', {'Variable': f'DEVICE_STATE(Custom:{user_uuid}-mobile)'}
            )
            assert_that(
                result,
                contains_exactly(
                    has_entries(
                        Response='Success',
                        Value='UNAVAILABLE',
                    )
                ),
            )

        until.assert_(user_hint_updated, timeout=10)
