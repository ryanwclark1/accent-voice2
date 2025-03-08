# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to
from sqlalchemy.inspection import inspect

from .helpers import fixtures
from .helpers.base import DBIntegrationTest, use_asset

UNKNOWN_NAME = 'unknown'


@use_asset('database')
class TestChannel(DBIntegrationTest):
    @fixtures.db.channel()
    @fixtures.db.channel()
    def test_find(self, channel, _):
        result = self._dao.channel.find(channel.name)
        assert_that(result, equal_to(channel))

        result = self._dao.channel.find(UNKNOWN_NAME)
        assert_that(result, equal_to(None))

    @fixtures.db.channel(state='ringing')
    def test_update(self, channel):
        state = 'undefined'
        channel.state = state
        self._dao.channel.update(channel)

        self._session.expire_all()
        assert_that(channel.state, equal_to(state))

    @fixtures.db.channel()
    @fixtures.db.channel()
    def test_delete_all(self, channel_1, channel_2):
        self._session.refresh(channel_1)
        self._session.refresh(channel_2)

        self._dao.channel.delete_all()

        assert_that(inspect(channel_1).deleted)
        assert_that(inspect(channel_2).deleted)
