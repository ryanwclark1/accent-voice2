# Copyright 2023 Accent Communications


from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    empty,
    equal_to,
    has_properties,
    none,
    not_,
)

from accent_dao.tests.test_dao import DAOTestCase

from ..dialaction import Dialaction
from ..dialpattern import DialPattern
from ..extension import Extension
from ..outcall import Outcall
from ..outcalltrunk import OutcallTrunk
from ..schedule import Schedule
from ..schedulepath import SchedulePath
from ..trunkfeatures import TrunkFeatures


class TestSchedules(DAOTestCase):

    def test_getter(self):
        outcall = self.add_outcall()
        schedule = self.add_schedule()
        self.add_schedule_path(path='outcall', pathid=outcall.id, schedule_id=schedule.id)

        row = self.session.query(Outcall).filter_by(id=outcall.id).first()
        assert_that(row, equal_to(outcall))
        assert_that(row.schedules, contains_exactly(schedule))

    def test_setter(self):
        outcall = self.add_outcall()
        schedule1 = self.add_schedule()
        schedule2 = self.add_schedule()
        outcall.schedules = [schedule1, schedule2]

        row = self.session.query(Outcall).filter_by(id=outcall.id).first()
        assert_that(row, equal_to(outcall))

        self.session.expire_all()
        assert_that(row.schedules, contains_inanyorder(schedule1, schedule2))

    def test_deleter(self):
        outcall = self.add_outcall()
        schedule1 = self.add_schedule()
        schedule2 = self.add_schedule()
        outcall.schedules = [schedule1, schedule2]
        self.session.flush()

        outcall.schedules = []

        row = self.session.query(Outcall).filter_by(id=outcall.id).first()
        assert_that(row, equal_to(outcall))
        assert_that(row.schedules, empty())

        row = self.session.query(Schedule).first()
        assert_that(row, not_(none()))

        row = self.session.query(SchedulePath).first()
        assert_that(row, none())


class TestDelete(DAOTestCase):

    def test_schedule_paths_are_deleted(self):
        outcall = self.add_outcall()
        schedule = self.add_schedule()
        self.add_schedule_path(schedule_id=schedule.id, path='outcall', pathid=outcall.id)

        self.session.delete(schedule)
        self.session.flush()

        row = self.session.query(SchedulePath).first()
        assert_that(row, none())

    def test_when_deleting_then_dialpattern_are_deleted(self):
        outcall = self.add_outcall()
        extension = self.add_extension()
        outcall.associate_extension(extension)

        self.session.delete(outcall)
        self.session.flush()

        dialpattern = self.session.query(DialPattern).first()
        assert_that(dialpattern, none())

    def test_dialaction_actions_are_deleted(self):
        outcall = self.add_outcall()
        self.add_dialaction(category='ivr_choice', action='outcall', actionarg1=outcall.id)
        self.add_dialaction(category='ivr', action='outcall', actionarg1=outcall.id)
        self.add_dialaction(category='user', action='outcall', actionarg1=outcall.id)
        self.add_dialaction(category='incall', action='outcall', actionarg1=outcall.id)

        self.session.delete(outcall)
        self.session.flush()

        row = self.session.query(Dialaction).first()
        assert_that(row, none())


class TestTrunks(DAOTestCase):

    def test_trunks_create(self):
        trunk = self.add_trunk()
        outcall_row = self.add_outcall()

        outcall_row.trunks = [trunk]

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.trunks, contains_inanyorder(trunk))

    def test_trunks_associate_order_by(self):
        outcall_row = self.add_outcall()
        trunk1_row = self.add_trunk()
        trunk2_row = self.add_trunk()
        trunk3_row = self.add_trunk()

        outcall_row.trunks = [trunk2_row, trunk3_row, trunk1_row]

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.trunks, contains_exactly(trunk2_row, trunk3_row, trunk1_row))

    def test_trunks_dissociate(self):
        outcall_row = self.add_outcall()
        trunk1_row = self.add_trunk()
        trunk2_row = self.add_trunk()
        trunk3_row = self.add_trunk()
        outcall_row.trunks = [trunk2_row, trunk3_row, trunk1_row]
        self.session.flush()

        outcall_row.trunks = []

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.trunks, empty())

        row = self.session.query(TrunkFeatures).first()
        assert_that(row, not_(none()))

        row = self.session.query(OutcallTrunk).first()
        assert_that(row, none())


class TestAssociateExtension(DAOTestCase):

    def test_associate_extension(self):
        extension = self.add_extension()
        outcall_row = self.add_outcall()

        outcall_row.associate_extension(extension,
                                        strip_digits=5,
                                        caller_id='toto',
                                        external_prefix='123',
                                        prefix='321')

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.context, equal_to(extension.context))
        assert_that(outcall.dialpatterns, contains_inanyorder(
            has_properties(strip_digits=5,
                           caller_id='toto',
                           external_prefix='123',
                           prefix='321',
                           type='outcall',
                           typeid=outcall.id,
                           exten=extension.exten,
                           extension=has_properties(exten=extension.exten,
                                                    context=extension.context,
                                                    type='outcall',
                                                    typeval=outcall.dialpatterns[0].id))
        ))

    def test_associate_multiple_extensions(self):
        outcall_row = self.add_outcall()
        extension1_row = self.add_extension()
        extension2_row = self.add_extension()
        extension3_row = self.add_extension()

        outcall_row.associate_extension(extension1_row, caller_id='toto')
        outcall_row.associate_extension(extension2_row, strip_digits=5)
        outcall_row.associate_extension(extension3_row, external_prefix='123', prefix='321')

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.extensions, contains_inanyorder(extension1_row, extension2_row, extension3_row))

    def test_associate_already_associated(self):
        outcall_row = self.add_outcall()
        extension_row = self.add_extension()
        outcall_row.associate_extension(extension_row)

        outcall_row.associate_extension(extension_row)

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.extensions, contains_inanyorder(extension_row))


class TestDissociateExtension(DAOTestCase):

    def test_dissociate_multiple_extensions(self):
        outcall_row = self.add_outcall()
        extension1_row = self.add_extension()
        extension2_row = self.add_extension()
        extension3_row = self.add_extension()
        outcall_row.associate_extension(extension1_row)
        outcall_row.associate_extension(extension2_row)
        outcall_row.associate_extension(extension3_row)
        self.session.flush()

        outcall_row.dissociate_extension(extension1_row)
        outcall_row.dissociate_extension(extension2_row)
        outcall_row.dissociate_extension(extension3_row)

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.extensions, empty())
        assert_that(outcall.context, none())

        rows = self.session.query(Extension).all()
        assert_that(rows, contains_inanyorder(has_properties(type='user', typeval='0'),
                                              has_properties(type='user', typeval='0'),
                                              has_properties(type='user', typeval='0')))

        row = self.session.query(DialPattern).first()
        assert_that(row, none())

    def test_dissociate_not_associated(self):
        outcall_row = self.add_outcall()
        extension_row = self.add_extension()

        outcall_row.dissociate_extension(extension_row)

        outcall = self.session.query(Outcall).filter_by(id=outcall_row.id).first()
        assert_that(outcall, equal_to(outcall_row))
        assert_that(outcall.extensions, empty())

        row = self.session.query(DialPattern).first()
        assert_that(row, none())


class TestUpdateExtensionAssociation(DAOTestCase):

    def test_update_extension_association(self):
        outcall_row = self.add_outcall()
        extension_row = self.add_extension()
        outcall_row.associate_extension(extension_row, caller_id='toto', prefix='1')

        outcall_row.update_extension_association(extension_row,
                                                 caller_id='tata',
                                                 external_prefix='123')

        rows = self.session.query(Extension).all()
        assert_that(rows, contains_exactly(extension_row))

        rows = self.session.query(DialPattern).all()
        assert_that(rows, contains_exactly(has_properties(
            caller_id='tata',
            external_prefix='123',
            prefix='1',
            strip_digits=0
        )))
