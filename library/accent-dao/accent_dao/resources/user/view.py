# file: accent_dao/resources/user/view.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import func, select
from sqlalchemy.sql import case

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.linefeatures import LineFeatures as Line
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures as User
from accent_dao.alchemy.voicemail import Voicemail
from accent_dao.helpers import errors
from accent_dao.resources.utils.view import View, ViewSelector

from .model import UserDirectory, UserSummary


class DefaultView(View):
    """Default view for user features."""

    async def query(self, session):
        """Define the query for the default view."""
        return select(User)

    def convert(self, row):
        """Convert a database row to a default view object."""
        return row


class DirectoryView(View):
    """View for directory information."""

    async def query(self, session):
        """Define the query for the directory view."""
        return select(
            User.id.label("id"),
            User.uuid.label("uuid"),
            UserLine.line_id.label("line_id"),
            User.agentid.label("agent_id"),
            User.firstname.label("firstname"),
            func.nullif(User.lastname, "").label("lastname"),
            func.nullif(User.email, "").label("email"),
            func.nullif(User.mobilephonenumber, "").label("mobile_phone_number"),
            Voicemail.mailbox.label("voicemail_number"),
            func.nullif(User.userfield, "").label("userfield"),
            func.nullif(User.description, "").label("description"),
            Extension.exten.label("exten"),
            Extension.context.label("context"),
        )

    def convert(self, row):
        """Convert a database row to a directory view object."""
        return UserDirectory(
            id=row.id,
            uuid=row.uuid,
            line_id=row.line_id,
            agent_id=row.agent_id,
            firstname=row.firstname,
            lastname=row.lastname,
            email=row.email,
            mobile_phone_number=row.mobile_phone_number,
            voicemail_number=row.voicemail_number,
            exten=row.exten,
            userfield=row.userfield,
            description=row.description,
            context=row.context,
        )


class SummaryView(View):
    """View for user summary information."""

    async def query(self, session):
        """Define the query for the summary view."""
        return select(
            User.id.label("id"),
            User.uuid.label("uuid"),
            User.firstname.label("firstname"),
            func.nullif(User.lastname, "").label("lastname"),
            func.nullif(User.email, "").label("email"),
            User.enabled.label("enabled"),
            case(
                (Line.endpoint_custom_id.isnot(None), None),
                else_=Line.provisioning_code,
            ).label("provisioning_code"),
            Line.protocol.label("protocol"),
            Extension.exten.label("extension"),
            Extension.context.label("context"),
        )

    def convert(self, row):
        """Convert a database row to a summary view object."""
        return UserSummary(
            id=row.id,
            uuid=row.uuid,
            firstname=row.firstname,
            lastname=row.lastname,
            email=row.email,
            enabled=row.enabled,
            extension=row.extension,
            context=row.context,
            provisioning_code=row.provisioning_code,
            protocol=row.protocol,
        )


class UserViewSelector(ViewSelector):
    """View selector for User resources."""

    def select(self, name=None, default_query=None):
        if not name:
            if default_query:
                return DefaultView(default_query)
            return self.default
        if name not in self.views:
            raise errors.invalid_view(name)
        return self.views[name]


user_view = UserViewSelector(
    default=DefaultView(), directory=DirectoryView(), summary=SummaryView()
)
