# Copyright 2023 Accent Communications

from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    equal_to,
    has_length,
    has_properties,
    is_not,
    none,
)

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.user_line import UserLine
from accent_dao.helpers.exception import InputError
from accent_dao.tests.test_dao import DAOTestCase

from .. import dao as user_line_dao


class TestFindBy(DAOTestCase):

    def test_given_column_does_not_exist_then_raises_error(self):
        self.assertRaises(InputError, user_line_dao.find_by, column=1)

    def test_find_by(self):
        user = self.add_user()
        line = self.add_line()
        expected = self.add_user_line(user_id=user.id, line_id=line.id)

        user_line = user_line_dao.find_by(user_id=expected.user_id)

        assert_that(user_line, equal_to(expected))


class TestFindAllByUserId(DAOTestCase):

    def test_find_all_by_user_id_no_user_line(self):
        expected_result = []
        result = user_line_dao.find_all_by_user_id(1)

        assert_that(result, equal_to(expected_result))

    def test_find_all_by_user_id(self):
        user = self.add_user()
        line = self.add_line()
        user_line = self.add_user_line(user_id=user.id, line_id=line.id)

        result = user_line_dao.find_all_by_user_id(user.id)

        assert_that(result, contains_exactly(user_line))

    def test_find_all_by_user_id_two_users(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        user_line_1 = self.add_user_line(
            user_id=user.id,
            line_id=line1.id,
            main_user=True,
            main_line=True,
        )
        user_line_2 = self.add_user_line(
            user_id=user.id,
            line_id=line2.id,
            main_user=True,
            main_line=False,
        )

        result = user_line_dao.find_all_by_user_id(user.id)

        assert_that(result, contains_inanyorder(user_line_1, user_line_2))


class TestFindMainUserLine(DAOTestCase):

    def test_find_main_user_line_no_user(self):
        line_id = 33

        result = user_line_dao.find_main_user_line(line_id)

        assert_that(result, equal_to(None))

    def test_find_main_user_line_no_line(self):
        self.add_user()
        line_id = 2

        result = user_line_dao.find_main_user_line(line_id)

        assert_that(result, equal_to(None))

    def test_find_main_user_line_one_user(self):
        user_line = self.add_user_line_without_exten()

        result = user_line_dao.find_main_user_line(user_line.line_id)

        assert_that(result.user_id, equal_to(user_line.user_id))

    def test_find_main_user_line(self):
        user1 = self.add_user()
        user2 = self.add_user()
        line = self.add_line()
        main_user_line = self.add_user_line(
            user_id=user1.id,
            line_id=line.id,
            main_user=True,
            main_line=True,
        )
        self.add_user_line(
            user_id=user2.id,
            line_id=line.id,
            main_user=False,
            main_line=True,
        )

        result = user_line_dao.find_main_user_line(line.id)

        assert_that(result, main_user_line)


class TestAssociateUserLine(DAOTestCase):

    def test_associate_user_with_line(self):
        user = self.add_user()
        line = self.add_line()

        result = user_line_dao.associate(user, line)

        assert_that(result, has_properties(
            user_id=user.id,
            line_id=line.id,
            main_user=True,
            main_line=True,
        ))

    def test_associate_user_with_line_already_associated(self):
        user = self.add_user()
        line = self.add_line()
        user_line_associated = user_line_dao.associate(user, line)

        result = user_line_dao.associate(user, line)

        assert_that(result, equal_to(user_line_associated))

    def test_associate_secondary_user_with_line(self):
        user1 = self.add_user()
        user2 = self.add_user()
        line = self.add_line()

        self.add_user_line(
            user_id=user1.id,
            line_id=line.id,
            main_user=True,
            main_line=True,
        )

        user_line_dao.associate(user2, line)

        result = (self.session.query(UserLine)
                  .filter(UserLine.line_id == line.id)
                  .all())

        assert_that(result, contains_inanyorder(
            has_properties(
                user_id=user1.id,
                line_id=line.id,
                main_user=True,
                main_line=True,
            ),
            has_properties(
                user_id=user2.id,
                line_id=line.id,
                main_user=False,
                main_line=True,
            ),
        ))

    def test_associate_user_with_secondary_line(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        self.add_user_line(user_id=user.id,
                           line_id=line1.id,
                           main_user=True,
                           main_line=True)

        user_line_dao.associate(user, line2)

        result = (self.session.query(UserLine)
                  .filter(UserLine.user_id == user.id)
                  .all())

        assert_that(result, contains_inanyorder(
            has_properties(
                user_id=user.id,
                line_id=line1.id,
                main_user=True,
                main_line=True,
            ),
            has_properties(
                user_id=user.id,
                line_id=line2.id,
                main_user=True,
                main_line=False,
            ),
        ))


class TestDissociateUserLine(DAOTestCase):

    def test_dissociate_user_line_with_queue_member(self):
        sip = self.add_endpoint_sip()
        user_line = self.add_user_line_with_queue_member(
            name_line=sip.name,
            endpoint_sip_uuid=sip.uuid,
        )

        user_line_dao.dissociate(user_line.user, user_line.line)

        result = (self.session.query(QueueMember)
                  .filter(QueueMember.usertype == 'user')
                  .filter(QueueMember.userid == user_line.user_id)
                  .first())

        assert_that(result, none())

    def test_dissociate_user_line(self):
        user = self.add_user()
        line = self.add_line()
        self.add_user_line(user_id=user.id, line_id=line.id)

        user_line_dao.dissociate(user, line)

        self.assert_user_line_deleted(user.id, line.id)

    def test_dissociate_user_line_not_associated(self):
        user = self.add_user()
        line = self.add_line()

        user_line_dao.dissociate(user, line)

        self.assert_user_line_deleted(user.id, line.id)

    def test_dissociate_secondary_user_line(self):
        user1 = self.add_user()
        user2 = self.add_user()
        line = self.add_line()
        self.add_user_line(
            user_id=user1.id,
            line_id=line.id,
            main_user=True,
        )
        self.add_user_line(
            user_id=user2.id,
            line_id=line.id,
            main_user=False,
        )

        user_line_dao.dissociate(user2, line)

        self.assert_user_line_associated(user1.id, line.id)
        self.assert_user_line_deleted(user2.id, line.id)

    def test_dissociate_user_secondary_line(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        self.add_user_line(
            user_id=user.id,
            line_id=line1.id,
            main_line=True,
        )
        self.add_user_line(
            user_id=user.id,
            line_id=line2.id,
            main_line=False,
        )

        user_line_dao.dissociate(user, line2)

        self.assert_user_line_associated(user.id, line1.id, main_line=True)
        self.assert_user_line_deleted(user.id, line2.id)

    def test_dissociate_user_main_line_when_has_secondary_line(self):
        user = self.add_user()
        line1 = self.add_line()
        line2 = self.add_line()
        self.add_user_line(
            user_id=user.id,
            line_id=line1.id,
            main_line=True,
        )
        self.add_user_line(
            user_id=user.id,
            line_id=line2.id,
            main_line=False,
        )

        user_line_dao.dissociate(user, line1)

        self.assert_user_line_deleted(user.id, line1.id)
        self.assert_user_line_associated(user.id, line2.id, main_line=True)

    def assert_user_line_associated(self, user_id, line_id, main_line=True):
        row = (self.session.query(UserLine)
               .filter(UserLine.user_id == user_id)
               .filter(UserLine.line_id == line_id)
               .filter(UserLine.main_line == main_line)
               .first())

        assert_that(row, is_not(none()))

    def assert_user_line_deleted(self, user_id, line_id):
        row = (self.session.query(UserLine)
               .filter(UserLine.user_id == user_id)
               .filter(UserLine.line_id == line_id)
               .first())

        assert_that(row, none())


class TestFindAllByLineId(DAOTestCase):

    def test_find_all_by_line_id_no_user_line(self):
        result = user_line_dao.find_all_by_line_id(1)

        assert_that(result, has_length(0))

    def test_find_all_by_line_id_one_user_line(self):
        user = self.add_user()
        line = self.add_line()
        user_line = self.add_user_line(user_id=user.id, line_id=line.id)

        result = user_line_dao.find_all_by_line_id(line.id)

        assert_that(result, contains_exactly(user_line))

    def test_find_all_by_line_id_two_user_lines(self):
        user1 = self.add_user()
        user2 = self.add_user()
        line = self.add_line()
        user_line_1 = self.add_user_line(
            user_id=user1.id,
            line_id=line.id,
            main_user=True,
        )
        user_line_2 = self.add_user_line(
            user_id=user2.id,
            line_id=line.id,
            main_user=False,
        )

        result = user_line_dao.find_all_by_line_id(line.id)

        assert_that(result, contains_inanyorder(user_line_1, user_line_2))


class TestAssociateAllLines(DAOTestCase):

    def test_associate_user_with_lines(self):
        user = self.add_user()
        line_1 = self.add_line()
        line_2 = self.add_line()

        result = user_line_dao.associate_all_lines(user, [line_1, line_2])

        assert_that(result, contains_exactly(
            has_properties(
                user_id=user.id,
                line_id=line_1.id,
                main_user=True,
                main_line=True,
            ),
            has_properties(
                user_id=user.id,
                line_id=line_2.id,
                main_user=True,
                main_line=False,
            ),
        ))

    def test_associate_secondary_user_with_line(self):
        user1 = self.add_user()
        user2 = self.add_user()
        line = self.add_line()

        self.add_user_line(
            user_id=user1.id,
            line_id=line.id,
            main_user=True,
            main_line=True,
        )

        user_line_dao.associate_all_lines(user2, [line])

        result = (self.session.query(UserLine)
                  .filter(UserLine.line_id == line.id)
                  .all())

        assert_that(result, contains_inanyorder(
            has_properties(
                user_id=user1.id,
                line_id=line.id,
                main_user=True,
                main_line=True,
            ),
            has_properties(
                user_id=user2.id,
                line_id=line.id,
                main_user=False,
                main_line=True,
            ),
        ))

    def test_dissociate_then_fixes_are_executed(self):
        sip = self.add_endpoint_sip()
        user = self.add_user()
        line = self.add_line(name=sip.name, endpoint_sip_uuid=sip.uuid)
        self.add_queue_member(
            userid=user.id,
            usertype='user',
            interface=f'PJSIP/{sip.name}',
        )
        self.add_user_line(line_id=line.id, user_id=user.id)

        user_line_dao.associate_all_lines(user, [])

        result = (self.session.query(QueueMember)
                  .filter(QueueMember.usertype == 'user')
                  .filter(QueueMember.userid == user.id)
                  .first())

        assert_that(result, none())

        result = (self.session.query(UserLine)
                  .filter(UserLine.user_id == user.id)
                  .filter(UserLine.line_id == line.id)
                  .first())

        assert_that(result, none())

    def test_associate_then_fixes_are_executed(self):
        user = self.add_user()
        line = self.add_line()
        extension = self.add_extension()
        self.add_line_extension(line_id=line.id, extension_id=extension.id)

        user_line_dao.associate_all_lines(user, [line])

        result = self.session.query(Extension).first()
        assert_that(result, has_properties({'type': 'user', 'typeval': str(user.id)}))
