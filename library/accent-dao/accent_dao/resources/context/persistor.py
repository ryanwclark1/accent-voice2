# Copyright 2023 Accent Communications

from accent_dao.alchemy.context import Context
from accent_dao.alchemy.contextmember import ContextMember
from accent_dao.helpers.persistor import BasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin


class ContextPersistor(CriteriaBuilderMixin, BasePersistor):
    _search_table = Context

    def __init__(self, session, context_search, tenant_uuids=None):
        self.session = session
        self.search_system = context_search
        self.tenant_uuids = tenant_uuids

    def _find_query(self, criteria):
        query = self.session.query(Context)
        if self.tenant_uuids is not None:
            query = query.filter(Context.tenant_uuid.in_(self.tenant_uuids))
        return self.build_criteria(query, criteria)

    def _search_query(self):
        return self.session.query(Context)

    def edit(self, context):
        self.session.add(context)
        self.session.flush()

    def delete(self, context):
        self._delete_associations(context)
        self.session.delete(context)
        self.session.flush()

    def _delete_associations(self, context):
        (
            self.session.query(ContextMember)
            .filter(ContextMember.context == context.name)
            .delete()
        )

    def associate_contexts(self, context, contexts):
        context.contexts = contexts
        self.session.flush()
