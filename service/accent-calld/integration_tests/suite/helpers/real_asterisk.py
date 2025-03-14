# Copyright 2023 Accent Communications

import ari
from accent_test_helpers import until
from ari.exceptions import ARINotFound, ARINotInStasis

from .amid import AmidClient
from .base import IntegrationTest, make_user_uuid
from .chan_test import ChanTest
from .constants import (
    ENDPOINT_AUTOANSWER,
    SOME_STASIS_APP,
    SOME_STASIS_APP_INSTANCE,
    VALID_TENANT,
    VALID_TOKEN,
)
from .wait_strategy import CalldAndAsteriskAndAmidWaitStrategy


class RealAsteriskIntegrationTest(IntegrationTest):
    asset = 'real_asterisk'
    wait_strategy = CalldAndAsteriskAndAmidWaitStrategy()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chan_test = ChanTest(cls.ari_config())

    @classmethod
    def make_amid(cls):
        return AmidClient(
            '127.0.0.1',
            cls.service_port(9491, 'amid'),
            prefix=None,
            https=False,
            token=VALID_TOKEN,
        )

    @classmethod
    def ari_config(cls):
        return {
            'base_url': 'http://127.0.0.1:{port}'.format(
                port=cls.service_port(5039, 'ari')
            ),
            'username': 'accent',
            'password': 'accent',
        }

    def ari_is_up(self):
        return ari.connect(**self.ari_config())

    def setUp(self):
        super().setUp()
        until.return_(self.ari_is_up, timeout=5)
        self.ari = ari.connect(**self.ari_config())
        self.reset_ari()

    def reconnect_ari(self):
        self.ari = ari.connect(**self.ari_config())

    def tearDown(self):
        super().tearDown()

    def reset_ari(self):
        for channel in self.ari.channels.list():
            try:
                channel.hangup()
            except (ARINotInStasis, ARINotFound):
                pass

        for bridge in self.ari.bridges.list():
            try:
                bridge.destroy()
            except (ARINotInStasis, ARINotFound):
                pass


class RealAsterisk:
    def __init__(self, ari, calld_client):
        self.ari = ari
        self.calld_client = calld_client

    def add_channel_to_bridge(self, bridge):
        def channel_is_in_stasis(channel_id):
            try:
                self.ari.channels.setChannelVar(
                    channelId=channel_id, variable='TEST_STASIS', value=''
                )
                return True
            except ARINotInStasis:
                return False

        new_channel = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            app=SOME_STASIS_APP,
            appArgs=[SOME_STASIS_APP_INSTANCE],
        )
        until.true(channel_is_in_stasis, new_channel.id, tries=2)
        bridge.addChannel(channel=new_channel.id)

        return new_channel

    def stasis_channel(self):
        def channel_is_in_stasis(channel_id):
            try:
                self.ari.channels.setChannelVar(
                    channelId=channel_id, variable='TEST_STASIS', value=''
                )
                return True
            except ARINotInStasis:
                return False

        new_channel = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            app=SOME_STASIS_APP,
            appArgs=[SOME_STASIS_APP_INSTANCE],
        )
        until.true(channel_is_in_stasis, new_channel.id, tries=2)

        return new_channel

    def given_bridged_call_stasis(
        self, caller_uuid=None, callee_uuid=None
    ) -> tuple[str, str]:
        bridge = self.ari.bridges.create(type='mixing')

        caller = self.stasis_channel()
        caller_uuid = caller_uuid or make_user_uuid()
        caller.setChannelVar(variable='ACCENT_USERUUID', value=caller_uuid)
        caller.setChannelVar(variable='ACCENT_TENANT_UUID', value=VALID_TENANT)
        bridge.addChannel(channel=caller.id)

        callee = self.stasis_channel()
        callee_uuid = callee_uuid or make_user_uuid()
        callee.setChannelVar(variable='ACCENT_USERUUID', value=callee_uuid)
        callee.setChannelVar(variable='ACCENT_TENANT_UUID', value=VALID_TENANT)
        bridge.addChannel(channel=callee.id)

        self.calld_client.set_token(VALID_TOKEN)

        def channels_have_been_created_in_calld(caller_id, callee_id):
            calls = self.calld_client.calls.list_calls(
                application=SOME_STASIS_APP,
                application_instance=SOME_STASIS_APP_INSTANCE,
            )
            channel_ids = [call['call_id'] for call in calls['items']]
            return caller_id in channel_ids and callee_id in channel_ids

        until.true(channels_have_been_created_in_calld, callee.id, caller.id, tries=5)

        return caller.id, callee.id

    def given_bridged_call_not_stasis(
        self, caller_uuid=None, callee_uuid=None, caller_variables=None
    ):
        caller_uuid = caller_uuid or make_user_uuid()
        callee_uuid = callee_uuid or make_user_uuid()
        variables = {
            'ACCENT_USERUUID': caller_uuid,
            '__CALLEE_ACCENT_USERUUID': callee_uuid,
            '__ACCENT_TENANT_UUID': VALID_TENANT,
        }
        variables.update(caller_variables or {})
        caller = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            context='local',
            extension='dial-autoanswer',
            variables={'variables': variables},
        )

        def bridged_channel(caller):
            try:
                bridge = next(
                    bridge
                    for bridge in self.ari.bridges.list()
                    if caller.id in bridge.json['channels']
                )
                callee_channel_id = next(
                    iter(set(bridge.json['channels']) - {caller.id})
                )
                return callee_channel_id
            except StopIteration:
                return False

        callee_channel_id = until.true(bridged_channel, caller, timeout=3)
        return caller.id, callee_channel_id

    def given_ringing_call_not_stasis(
        self, caller_uuid=None, callee_uuid=None, caller_variables=None
    ):
        caller_uuid = caller_uuid or make_user_uuid()
        callee_uuid = callee_uuid or make_user_uuid()
        variables = {
            'ACCENT_USERUUID': caller_uuid,
            '__CALLEE_ACCENT_USERUUID': callee_uuid,
            '__ACCENT_TENANT_UUID': VALID_TENANT,
        }
        variables.update(caller_variables or {})
        caller = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            context='local',
            extension='recipient',
            variables={'variables': variables},
        )

        def ringing_channel(caller):
            channels = self.ari.channels.list()
            try:
                callee_channel_id = next(
                    channel.id
                    for channel in channels
                    # the caller is in ringing state for a short time due to originate
                    if channel.json['state'] == 'Ringing' and channel.id != caller.id
                )
                return callee_channel_id
            except StopIteration:
                return False

        callee_channel_id = until.true(
            ringing_channel, caller, timeout=3, message='Could not find ringing channel'
        )
        return caller.id, callee_channel_id

    def pickup(self, user_uuid=None):
        user_uuid = user_uuid or make_user_uuid()
        variables = {
            'ACCENT_USERUUID': user_uuid,
            '__ACCENT_TENANT_UUID': VALID_TENANT,
        }
        interceptor = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            context='local',
            extension='pickup',
            variables={'variables': variables},
        )
        return interceptor.id
