# Copyright 2023 Accent Communications

from hamcrest import assert_that, has_entries, is_not, none

from . import confd


def test_get():
    response = confd.infos.get()
    assert_that(
        response.item, has_entries(uuid=is_not(none()), accent_version=is_not(none()))
    )
