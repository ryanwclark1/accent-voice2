# Copyright 2023 Accent Communications


from hamcrest import (
    assert_that,
    contains_exactly,
    contains_inanyorder,
    empty,
    equal_to,
    has_properties,
)

from accent_dao.alchemy.features import Features
from accent_dao.helpers.exception import NotFoundError
from accent_dao.tests.test_dao import DAOTestCase

from .. import dao as features_dao


class TestFindAll(DAOTestCase):

    def test_find_all_no_features_general(self):
        result = features_dao.find_all('general')

        assert_that(result, empty())

    def test_find_all(self):
        row1 = self.add_features(var_metric=3,
                                 var_name='setting1',
                                 var_val='value1')
        row2 = self.add_features(var_metric=2,
                                 var_name='setting2',
                                 var_val='value1')
        row3 = self.add_features(var_metric=1,
                                 var_name='setting3',
                                 var_val='value1')
        row4 = self.add_features(var_metric=4,
                                 var_name='setting2',
                                 var_val='value2')

        features = features_dao.find_all('general')

        assert_that(features, contains_exactly(row3, row2, row1, row4))

    def test_find_all_do_not_find_var_val_none(self):
        self.add_features(var_name='setting1',
                          var_val=None)
        row2 = self.add_features(var_name='setting1',
                                 var_val='value1')

        features = features_dao.find_all('general')

        assert_that(features, contains_inanyorder(row2))

    def test_find_all_do_not_find_other_section(self):
        self.add_features(category='not_general')
        row2 = self.add_features(var_name='setting1',
                                 var_val='value1')

        features = features_dao.find_all('general')

        assert_that(features, contains_inanyorder(row2))


class TestEditAll(DAOTestCase):

    def test_edit_all(self):
        row1 = Features(var_name='setting1', var_val='value1')
        row2 = Features(var_name='setting2', var_val='value1')
        row3 = Features(var_name='setting3', var_val='value1')
        row4 = Features(var_name='setting4', var_val='value1')

        features_dao.edit_all('general', [row1, row2, row3, row4])

        features = features_dao.find_all('general')
        assert_that(features, contains_inanyorder(row1, row2, row3, row4))

    def test_delete_old_entries(self):
        self.add_features()
        self.add_features()
        row = Features(var_name='nat', var_val='value1', category='general')

        features_dao.edit_all('general', [row])

        features = features_dao.find_all('general')
        assert_that(features, contains_inanyorder(row))

    def test_does_not_change_foreign_key_id(self):
        feature1 = self.add_features(category='featuremap', var_name='blindxfer', var_val='value1')
        feature2 = self.add_features(category='featuremap', var_name='atxfer', var_val='value2')
        feature3 = self.add_features(category='applicationmap', var_name='togglerecord', var_val='value3')

        row1 = Features(var_name='blindxfer', var_val='other_value1')
        row2 = Features(var_name='atxfer', var_val='other_value2')
        row3 = Features(var_name='togglerecord', var_val='other_value3')

        features_dao.edit_all('featuremap', [row1, row2])
        features_dao.edit_all('applicationmap', [row3])

        features = features_dao.find_all('featuremap')
        assert_that(features, contains_inanyorder(
            has_properties(id=feature1.id,
                           var_val=row1.var_val),
            has_properties(id=feature2.id,
                           var_val=row2.var_val),
        ))
        features = features_dao.find_all('applicationmap')
        assert_that(features, contains_inanyorder(
            has_properties(id=feature3.id,
                           var_val=row3.var_val),
        ))

class TestGetValue(DAOTestCase):

    def test_when_getting_feature_by_id_then_returns_value(self):
        self.add_features(id=12, var_name='pickupexten', var_val='*8')

        result = features_dao.get_value(12)

        assert_that(result, equal_to('*8'))

    def test_given_no_features_then_raises_error(self):
        self.assertRaises(NotFoundError, features_dao.get_value, 12)
