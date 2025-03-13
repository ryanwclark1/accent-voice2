# file: accent_dao/resources/line/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import and_, func, or_
from sqlalchemy.orm.query import Query
from sqlalchemy.types import String

from accent_dao.alchemy.endpoint_sip import EndpointSIP, EndpointSIPSection
from accent_dao.alchemy.endpoint_sip_section_option import (
    EndpointSIPSectionOption,
)
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class CustomLineSearchSystem(SearchSystem):
    """Extend SearchSystem to work around lack of callerid field."""

    def search_from_query(self, query, parameters: dict = None):
        """Perform a search on the given query, accounting for complex caller ID logic.

        This method modifies the provided SQLAlchemy query object by joining it with
        several related tables to access caller ID information. It then applies filters
        based on the provided parameters.

        Parameters
        ----------
        query : sqlalchemy.orm.query.Query
            The initial query object to be modified.
        parameters : dict, optional
            A dictionary of search parameters. Supported keys:
            - "search": A string to search for in the name, description,
                provisioning ID, or caller ID.
            - "exten": A string to search for in the extension.

        Returns
        -------
        sqlalchemy.orm.query.Query
            The modified query object with the applied filters.

        """
        # Join LineFeatures with EndpointSIP and related tables to access callerid
        query = query.outerjoin(
            EndpointSIP, LineFeatures.endpoint_sip_uuid == EndpointSIP.uuid
        )
        query = query.outerjoin(
            EndpointSIPSection,
            EndpointSIP.uuid == EndpointSIPSection.endpoint_sip_uuid,
        )
        query = query.outerjoin(
            EndpointSIPSectionOption,
            and_(
                EndpointSIPSection.uuid
                == EndpointSIPSectionOption.endpoint_sip_section_uuid,
                EndpointSIPSectionOption.key == "callerid",
            ),
        )

        if parameters and "search" in parameters:
            search_term = f"%{parameters['search']}%"

            # Modified query for callerid search logic
            callerid_query = func.concat(
                '"',
                func.substring(EndpointSIPSectionOption.value, '"(.*?)"'),
                '" <',
                func.substring(EndpointSIPSectionOption.value, "<(.*?)>"),
                ">",
            ).ilike(search_term)

            query = query.filter(
                or_(
                    LineFeatures.name.ilike(search_term),
                    LineFeatures.description.ilike(search_term),
                    LineFeatures.provisioningid.cast(String).ilike(search_term),
                    callerid_query,
                )
            )

        if parameters and "exten" in parameters:
            # Join with Extension table and add the filter
            query = query.outerjoin(
                LineExtension, LineFeatures.id == LineExtension.line_id
            ).outerjoin(Extension, LineExtension.extension_id == Extension.id)
            query = query.filter(Extension.exten.ilike(f"%{parameters['exten']}%"))

        return super().search_from_query(query, parameters)


config = SearchConfig(
    table=LineFeatures,
    columns={
        "context": LineFeatures.context,
        "provisioningid": LineFeatures.provisioningid,
        "provisioning_code": LineFeatures.provisioning_code,
        "position": LineFeatures.num,
        "device_slot": LineFeatures.num,
        "protocol": LineFeatures.protocol,
        "device_id": LineFeatures.device_id,
        "name": LineFeatures.name,
        "caller_id_name": LineFeatures.caller_id_name,
        "caller_id_num": LineFeatures.caller_id_num,
        "exten": Extension.exten,
    },
    search=[
        "name",
        "description",
        "caller_id_name",
        "caller_id_num",
        "provisioningid",
    ],
    default_sort="name",
)

line_search = CustomLineSearchSystem(config)
