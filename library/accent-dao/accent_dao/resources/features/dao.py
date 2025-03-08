# Copyright 2023 Accent Communications

from accent_dao.alchemy.features import Features
from accent_dao.helpers import errors
from accent_dao.helpers.db_manager import daosession

from .persistor import FeaturesPersistor


@daosession
def find_all(session, section):
    return FeaturesPersistor(session).find_all(section)


@daosession
def edit_all(session, section, features):
    FeaturesPersistor(session).edit_all(section, features)


@daosession
def get_value(session, feature_id):
    value = session.query(Features.var_val).filter(Features.id == feature_id).scalar()

    if not value:
        raise errors.not_found('Features', id=feature_id)

    value = _extract_applicationmap_dtmf(value)

    return value


def _extract_applicationmap_dtmf(value):
    return value.split(',', 1)[0]
