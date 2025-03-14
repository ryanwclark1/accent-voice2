# Copyright 2023 Accent Communications

from uuid import uuid4

from accent_test_helpers import until
from ari.exceptions import ARINotFound

from .helpers.constants import ENDPOINT_AUTOANSWER
from .helpers.real_asterisk import RealAsteriskIntegrationTest


class TestDialMobile(RealAsteriskIntegrationTest):
    asset = 'real_asterisk'

    def test_that_dial_mobile_join_with_no_bridge_does_not_block(self):
        unknown_bridge_id = str(uuid4())
        channel = self.ari.channels.originate(
            endpoint=ENDPOINT_AUTOANSWER,
            app='dial_mobile',
            appArgs=['join', unknown_bridge_id],
        )

        def channel_is_gone(ari, channel_id):
            try:
                ari.channels.get(channelId=channel_id)
                return False
            except ARINotFound:
                return True

        until.true(
            channel_is_gone,
            self.ari,
            channel.id,
            timeout=10,
            message='Channel is stuck in stasis',
        )
