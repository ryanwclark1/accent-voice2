# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch
from unittest.mock import sentinel as s

from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, not_

from ..stasis import ApplicationStasis


class TestApplicationStasisStartHandler(TestCase):
    def setUp(self):
        self.ari = Mock()
        self.service = Mock()
        self.notifier = Mock()
        self.confd_apps_cache = Mock()
        self.moh_cache = Mock()

        self.app = ApplicationStasis(
            self.ari,
            self.service,
            self.notifier,
            self.confd_apps_cache,
            self.moh_cache,
        )

    def test_stasis_start_no_a_accent_app(self):
        event = {'application': 'foobar'}

        assert_that(
            calling(self.app.stasis_start).with_args(s.event_object, event),
            not_(raises(Exception)),
        )

    def test_stasis_start_user_outgoing_call(self):
        uuid = 'e3f9b7ef-3fa7-4240-88f1-e6f5c0945b9b'
        event = {
            'application': f'accent-app-{uuid}',
            'args': [],
        }

        with patch.object(self.app, '_stasis_start_user_outgoing') as fn:
            self.app.stasis_start(s.event_object, event)

            fn.assert_called_once_with(uuid, s.event_object, event)

    def test_stasis_start_incoming_call(self):
        uuid = 'e3f9b7ef-3fa7-4240-88f1-e6f5c0945b9b'
        event = {
            'application': f'accent-app-{uuid}',
            'args': ['incoming'],
        }

        with patch.object(self.app, '_stasis_start_incoming') as fn:
            self.app.stasis_start(s.event_object, event)

            fn.assert_called_once_with(uuid, s.event_object, event)

    def test_stasis_start_originate_in_node(self):
        uuid = 'e3f9b7ef-3fa7-4240-88f1-e6f5c0945b9b'
        node_uuid = 'a39a50e5-b5dc-4816-ab6a-1c5b9305e513'
        event = {
            'application': f'accent-app-{uuid}',
            'args': ['originate', node_uuid],
        }

        with patch.object(self.app, '_stasis_start_originate') as fn:
            self.app.stasis_start(s.event_object, event)

            fn.assert_called_once_with(uuid, node_uuid, s.event_object, event)

    def test_stasis_start_originate_no_node(self):
        uuid = 'e3f9b7ef-3fa7-4240-88f1-e6f5c0945b9b'
        event = {'application': f'accent-app-{uuid}', 'args': ['originate']}

        with patch.object(self.app, '_stasis_start_originate') as fn:
            self.app.stasis_start(s.event_object, event)

            fn.assert_called_once_with(uuid, None, s.event_object, event)
