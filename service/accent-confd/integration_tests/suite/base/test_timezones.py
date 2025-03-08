# Copyright 2023 Accent Communications

from hamcrest import assert_that, has_items, not_

from . import confd


def test_get():
    response = confd.timezones.get()
    response.assert_ok()

    assert_that(response.items, has_items({'zone_name': 'America/Montreal'}))
    assert_that(response.total, not_(0))
