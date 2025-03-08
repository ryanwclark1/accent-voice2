# Copyright 2023 Accent Communications

from sqlalchemy.sql.expression import and_

from accent_dao.alchemy.accessfeatures import AccessFeatures
from accent_dao.helpers.db_manager import daosession


@daosession
def get_authorized_subnets(session):
    rows = (
        session.query(AccessFeatures.host)
        .filter(
            and_(AccessFeatures.feature == 'phonebook', AccessFeatures.commented == 0)
        )
        .all()
    )
    return [row.host for row in rows]
