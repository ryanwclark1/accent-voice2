# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from ..stasis import SwitchboardsStasis


class TestStasis(TestCase):
    def test_unhandled_error_during_stasis(self):
        ari, confd, notifier, service = Mock(), Mock(), Mock(), Mock()
        stasis = SwitchboardsStasis(ari, confd, notifier, service)
        channel = Mock()

        event = {
            'args': ['switchboard', 'switchboard_queue']
        }  # The second argument is missing
        event_objects = {'channel': channel}

        with patch.object(stasis, '_stasis_start_queue', Mock(side_effect=Exception)):
            stasis.stasis_start(event_objects, event)

        ari.client.channels.continueInDialplan.assert_called_once_with(
            channelId=channel.id
        )
