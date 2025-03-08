# Copyright 2023 Accent Communications

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_
from hamcrest import none

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.resources.directory_profile import dao as profile_dao

from accent_dao.tests.test_dao import DAOTestCase


class TestDirectoryProfileDao(DAOTestCase):

    def test_find_by_incall_id(self):
        user_line = self.add_user_line_with_exten()
        incall = self.add_incall(destination=Dialaction(action='user', actionarg1=user_line.user_id))
        result = profile_dao.find_by_incall_id(incall_id=incall.id)

        assert_that(result.profile, equal_to(user_line.line.context))
        assert_that(result.accent_user_uuid, equal_to(user_line.user.uuid))

    def test_find_by_incall_id_return_none_when_not_found(self):

        result = profile_dao.find_by_incall_id(incall_id=99999999)

        assert_that(result, is_(none()))
