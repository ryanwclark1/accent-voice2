# Copyright 2023 Accent Communications

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.pjsip_transport import PJSIPTransport
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult


class TransportPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = PJSIPTransport

    def __init__(self, session, transport_search):
        self.session = session
        self.transport_search = transport_search

    def delete(self, transport, fallback=None):
        if fallback:
            self._update_transport(transport, fallback)
        self.session.delete(transport)
        self.session.flush()

    def _update_transport(self, current, new):
        (
            self.session.query(EndpointSIP)
            .filter(EndpointSIP.transport_uuid == current.uuid)
            .update({'transport_uuid': new.uuid})
        )

    def get_by(self, criteria):
        model = self.find_by(criteria)
        if not model:
            raise errors.not_found('Transport', **criteria)
        return model

    def search(self, parameters):
        rows, total = self.transport_search.search(self.session, parameters)
        return SearchResult(total, rows)

    def _find_query(self, criteria):
        query = self.session.query(PJSIPTransport)
        return self.build_criteria(query, criteria)
