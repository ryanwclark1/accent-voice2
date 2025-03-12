# Copyright 2023 Accent Communications

import logging

from sqlalchemy import and_

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import daosession

logger = logging.getLogger(__name__)


@daosession
def get(session, user_id) -> UserFeatures:
    """Retrieve a user by their ID.

    Args:
        session: The database session.
        user_id: The ID of the user, which can be an integer or a UUID.

    Returns:
        UserFeatures: The user features object if found.

    Raises:
        LookupError: If no user is found with the given ID.

    """
    if isinstance(user_id, int):
        result = session.query(UserFeatures).filter(UserFeatures.id == user_id).first()
    else:
        result = session.query(UserFeatures).filter(UserFeatures.uuid == user_id).first()
    if result is None:
        raise LookupError
    return result


@daosession
def get_user_by_agent_id(session, agent_id):
    result = session.query(UserFeatures).filter(UserFeatures.agent_id == agent_id).first()
    if not result:
        raise LookupError
    return result


@daosession
def get_user_by_number_context(session, exten, context):
    user = (session.query(UserFeatures)
            .join(Extension, and_(Extension.context == context,
                                  Extension.exten == exten,
                                  Extension.commented == 0))
            .join(LineExtension, LineExtension.extension_id == Extension.id)
            .join(UserLine, and_(UserLine.user_id == UserFeatures.id,
                                 UserLine.line_id == LineExtension.line_id,
                                 UserLine.main_line == True))  # noqa
            .join(LineFeatures, and_(LineFeatures.commented == 0))
            .first())

    if not user:
        raise LookupError("No user with number %s in context %s", (exten, context))

    return user
