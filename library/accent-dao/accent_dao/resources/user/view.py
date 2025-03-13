# Copyright 2025 Accent Communications

from sqlalchemy import func, select

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.endpoint_sip_options_view import EndpointSIPOptionsView
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.resources.utils.view import View, ViewSelector


class DefaultView(View):
    """Default view for UserFeatures."""

    def query(self, session):
        """Return the query for default view."""
        return session.query(UserFeatures)

    def convert(self, row):
        """Return the row as is."""
        return row


class DirectoryView(View):
    """View for directory information of UserFeatures."""

    def query(self, session):
        """Define the query for the directory view."""
        query = session.query(
            UserFeatures.id.label("id"),
            UserFeatures.uuid.label("uuid"),
            UserLine.line_id.label("line_id"),
            UserFeatures.agentid.label("agent_id"),
            UserFeatures.firstname.label("firstname"),
            func.nullif(UserFeatures.lastname, "").label("lastname"),
            func.nullif(UserFeatures.email, "").label("email"),
            func.nullif(UserFeatures.mobilephonenumber, "").label(
                "mobile_phone_number"
            ),
            func.nullif(UserFeatures.voicemail, "").label(
                "voicemail_number"
            ),  # Use property
            func.nullif(UserFeatures.userfield, "").label("userfield"),
            func.nullif(UserFeatures.description, "").label("description"),
            Extension.exten.label("exten"),
            Extension.context.label("context"),
        )
        return query

    def convert(self, row):
        """Convert database row to UserDirectory model."""
        from .model import UserDirectory  # Local import to prevent circular import

        return UserDirectory(
            id=row.id,
            uuid=str(row.uuid),
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
    """View for summary information of UserFeatures."""

    def query(self, session):
        """Define the query for the summary view."""
        query = session.query(
            UserFeatures.id.label("id"),
            UserFeatures.uuid.label("uuid"),
            UserFeatures.firstname.label("firstname"),
            func.nullif(UserFeatures.lastname, "").label("lastname"),
            func.nullif(UserFeatures.email, "").label("email"),
            UserFeatures.enabled.label("enabled"),
            LineFeatures.provisioning_code.label("provisioning_code"),  # Use property
            LineFeatures.protocol.label("protocol"),  # Use property
            Extension.exten.label("extension"),
            Extension.context.label("context"),
        )
        return query

    def convert(self, row):
        """Convert database row to UserSummary model."""
        from .model import UserSummary  # Local import to prevent circular import

        return UserSummary(
            id=row.id,
            uuid=str(row.uuid),  # Convert UUID to string
            firstname=row.firstname,
            lastname=row.lastname,
            email=row.email,
            enabled=row.enabled,
            extension=row.extension,
            context=row.context,
            provisioning_code=row.provisioning_code,
            protocol=row.protocol,
        )


user_view = ViewSelector(
    default=DefaultView(), directory=DirectoryView(), summary=SummaryView()
)
