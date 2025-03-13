# Copyright 2025 Accent Communications

from sqlalchemy import or_

from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class UserSearchSystem(SearchSystem):
    """Search system for UserFeatures, adds search on UUID."""

    def search_from_query(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        if uuid_param := parameters.pop("uuid", None):
            uuids = [uuid for uuid in uuid_param.split(",") if self.is_valid_uuid(uuid)]
            query = self._filter_exact_match_uuids(query, uuids)
        return super().search_from_query(query, parameters)

    def _filter_exact_match_uuids(self, query, uuids):
        if not uuids:
            return query.filter(False)  # No valid UUIDs, return no results
        else:
            return query.filter(
                or_(UserFeatures.uuid.in_(uuids), UserFeatures.id.in_(uuids))
            )

    def is_valid_uuid(self, uuid_string):
        """Validate if the provided string is a valid UUID."""
        try:
            uuid_obj = UUID(uuid_string, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_string

    def search_from_query_collated(self, query, parameters=None):
        query = query.collate("C")
        return self.search_from_query(query, parameters)


config = SearchConfig(
    table=UserFeatures,
    columns={
        "id": UserFeatures.id,
        "uuid": UserFeatures.uuid,
        "firstname": UserFeatures.firstname,
        "lastname": UserFeatures.lastname,
        "fullname": UserFeatures.fullname,
        "caller_id": UserFeatures.callerid,
        "description": UserFeatures.description,
        "userfield": UserFeatures.userfield,
        "email": UserFeatures.email,
        "mobile_phone_number": UserFeatures.mobilephonenumber,
        "music_on_hold": UserFeatures.musiconhold,
        "outgoing_caller_id": UserFeatures.outgoing_caller_id,
        "preprocess_subroutine": UserFeatures.preprocess_subroutine,
        "voicemail_number": UserFeatures.voicemail,  # Assuming this is a property/column_property
        "provisioning_code": UserFeatures.provisioning_code,  # Assuming this exists
        "exten": UserFeatures.exten,  # Assuming this exists and is correctly defined
        "username": UserFeatures.username,
        "enabled": UserFeatures.enabled,
        # Add other columns as needed for sorting/filtering
    },
    search=[
        "firstname",
        "lastname",
        "fullname",
        "caller_id",
        "description",
        "userfield",
        "email",
        "mobile_phone_number",
        "preprocess_subroutine",
        "outgoing_caller_id",
        "exten",  # Include exten in searchable fields
        "username",  # Include username in searchable fields
        "provisioning_code",
    ],
    default_sort="lastname",
)

user_search = UserSearchSystem(config)
