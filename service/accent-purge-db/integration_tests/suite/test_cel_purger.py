# Copyright 2023 Accent Communications

from datetime import datetime, timedelta

from accent_dao.alchemy.cel import CEL as CELSchema
from accent_dao.tests.test_dao import DAOTestCase
from hamcrest import assert_that, contains_inanyorder, empty, has_property

from accent_purge_db.table_purger import CELPurger


class TestCELPurger(DAOTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_that_CELPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 1))
        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 2))
        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, empty())

    def test_that_CELPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(
            result,
            contains_inanyorder(
                has_property('id', id_entry0),
                has_property('id', id_entry1),
                has_property('id', id_entry2),
            ),
        )

    def test_that_CELPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(
            result,
            contains_inanyorder(has_property('id', id_entry1), has_property('id', id_entry2)),
        )

    def test_that_CELPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, empty())
