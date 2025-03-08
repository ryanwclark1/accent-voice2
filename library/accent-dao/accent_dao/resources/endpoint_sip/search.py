# Copyright 2023 Accent Communications

import uuid

from sqlalchemy.sql import text

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=EndpointSIP,
    columns={
        'name': EndpointSIP.name,
        'asterisk_id': EndpointSIP.asterisk_id,
        'label': EndpointSIP.label,
        'template': EndpointSIP.template,
    },
    default_sort='label',
)


class EndpointSIPSearchSystem(SearchSystem):
    def search_from_query(self, query, parameters=None):
        if isinstance(parameters, dict):
            if uuid_param := parameters.pop('uuid', None):
                uuids = [uuid for uuid in uuid_param.split(',') if is_valid_uuid(uuid)]
                query = self._filter_exact_match_uuids(query, uuids)
            return super().search_from_query(query, parameters)

    def _filter_exact_match_uuids(self, query, uuids):
        if not uuids:
            return query.filter(text('false'))
        else:
            return query.filter(EndpointSIP.uuid.in_(uuids))


def is_valid_uuid(input):
    try:
        uuid.UUID(input)
        return True
    except ValueError:
        return False


sip_search = EndpointSIPSearchSystem(config)
