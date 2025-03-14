# Copyright 2023 Accent Communications

import json
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import sentinel as s

from ari.exceptions import ARINotFound
from hamcrest import assert_that, calling, equal_to, has_property, is_not, raises

from ..state_persistor import ChannelCacheEntry, ReadOnlyStatePersistor, StatePersistor

SOME_CHANNEL_ID = 'some-channel-id'


class TestChannelCacheEntry(TestCase):
    def test_to_dict(self):
        entry = ChannelCacheEntry(s.app, s.app_instance, s.state)

        assert_that(
            entry.to_dict(),
            equal_to({'app': s.app, 'app_instance': s.app_instance, 'state': s.state}),
        )

    def test_from_dict(self):
        entry = ChannelCacheEntry.from_dict(
            {'app': s.app, 'app_instance': s.app_instance, 'state': s.state}
        )

        assert_that(entry.app, equal_to(s.app))
        assert_that(entry.app_instance, equal_to(s.app_instance))
        assert_that(entry.state, equal_to(s.state))


class TestReadOnlyStatePersistor(TestCase):
    def setUp(self):
        self.ari = Mock()
        self.persistor = ReadOnlyStatePersistor(self.ari)

    def test_read_only_state_persistor_cant_upsert(self):
        assert_that(self.persistor, is_not(has_property('upsert')))

    def test_read_only_state_persistor_cant_remove(self):
        assert_that(self.persistor, is_not(has_property('remove')))

    def test_given_no_calls_when_get_unknown_channel_then_raise_keyerror(self):
        self.ari.asterisk.getGlobalVar.side_effect = ARINotFound(Mock(), Mock())

        assert_that(
            calling(self.persistor.get).with_args('unknown-channel-id'),
            raises(KeyError),
        )

    def test_given_valid_cache_when_get_existing_channel_then_return_entry(self):
        self.ari.asterisk.getGlobalVar.return_value = {
            'value': json.dumps(
                {'app': 'myapp', 'app_instance': 'red', 'state': 'mystate'}
            )
        }
        result = self.persistor.get('my-channel')

        assert_that(result.state, equal_to('mystate'))


class TestStatePersistor(TestCase):
    def setUp(self):
        self.ari = Mock()
        self.persistor = StatePersistor(self.ari)

    def test_when_upsert_then_variable_set(self):
        entry = Mock()
        entry.to_dict.return_value = 'my-entry'
        exptected_variable = '"my-entry"'

        self.persistor.upsert(SOME_CHANNEL_ID, entry)

        self.ari.asterisk.setGlobalVar.assert_called_once_with(
            variable=f'ACCENT_CHANNELS_{SOME_CHANNEL_ID}',
            value=exptected_variable,
        )

    def test_when_remove_then_variable_is_deleted(self):
        self.persistor.remove(SOME_CHANNEL_ID)

        self.ari.asterisk.setGlobalVar.assert_called_once_with(
            variable=f'GLOBAL_DELETE(ACCENT_CHANNELS_{SOME_CHANNEL_ID})', value=''
        )

    def test_given_no_calls_when_get_then_raise_keyerror(self):
        self.ari.asterisk.getGlobalVar.side_effect = ARINotFound(Mock(), Mock())

        assert_that(
            calling(self.persistor.get).with_args('unknown-channel-id'),
            raises(KeyError),
        )

    def test_given_existing_channel_when_get_then_return_entry(self):
        self.ari.asterisk.getGlobalVar.return_value = {
            'value': json.dumps(
                {'app': 'myapp', 'app_instance': 'red', 'state': 'mystate'}
            )
        }
        result = self.persistor.get('my-channel')

        assert_that(result.state, equal_to('mystate'))
