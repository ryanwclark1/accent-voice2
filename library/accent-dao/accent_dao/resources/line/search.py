# Copyright 2023 Accent Communications

from sqlalchemy.sql.elements import and_

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=LineFeatures,
    columns={
        'context': LineFeatures.context,
        'provisioning_code': LineFeatures.provisioningid,
        'provisioning_extension': LineFeatures.provisioningid,
        'position': LineFeatures.num,
        'device_slot': LineFeatures.num,
        'protocol': LineFeatures.protocol,
        'device_id': LineFeatures.device,
        'name': LineFeatures.name,
        'caller_id_name': LineFeatures.caller_id_name,
        'caller_id_num': LineFeatures.caller_id_num,
        'exten': Extension.exten,
    },
    default_sort='name',
)


class LineSearchSystem(SearchSystem):
    def search_from_query(self, query, parameters):
        query = self._search_on_extension(query)
        return super().search_from_query(query, parameters)

    def _search_on_extension(self, query):
        return query.outerjoin(
            LineExtension,
            and_(LineExtension.line_id == LineFeatures.id, LineFeatures.commented == 0),
        ).outerjoin(
            Extension,
            and_(
                LineExtension.extension_id == Extension.id,
                LineExtension.line_id == LineFeatures.id,
                Extension.commented == 0,
            ),
        )


line_search = LineSearchSystem(config)
