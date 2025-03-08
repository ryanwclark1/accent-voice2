# Copyright 2023 Accent Communications

from sqlalchemy import Integer
from sqlalchemy.sql import cast

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import daosession


@daosession
def find_by_incall_id(session, incall_id):
    row = (
        session.query(
            UserFeatures.uuid.label('accent_user_uuid'),
            LineFeatures.context.label('profile'),
        ).filter(
            Dialaction.category == 'incall',
            Dialaction.categoryval == str(incall_id),
            Dialaction.action == 'user',
            UserFeatures.id == cast(Dialaction.actionarg1, Integer),
            UserLine.user_id == UserFeatures.id,
            UserLine.line_id == LineFeatures.id,
            UserLine.main_line.is_(True),
            UserLine.main_user.is_(True),
        )
    ).first()
    return row
