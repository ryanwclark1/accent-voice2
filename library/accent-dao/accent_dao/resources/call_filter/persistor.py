# file: accent_dao/resources/call_filter/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.callfilter import Callfilter
from accent_dao.alchemy.callfiltermember import Callfiltermember
from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence



class CallFilterPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Callfilter]):
    """Persistor class for Callfilter model."""

    _search_table = Callfilter

    def __init__(
        self,
        session: AsyncSession,
        call_filter_search: Any,
        tenant_uuids: list[str] | None = None,  # Added missing type hint
    ) -> None:
        """Initialize CallFilterPersistor.

        Args:
            session: Async database session.
            call_filter_search: Search system for call filters.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.call_filter_search = call_filter_search
        self.tenant_uuids = tenant_uuids
        self.session = session  # Retain for use in custom methods.

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find call filters based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Callfilter)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Callfilter:
        """Retrieve a single call filter by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Callfilter: The found call filter.

        Raises:
            NotFoundError: If no call filter is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("Callfilter", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for call filters.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = select(self.call_filter_search.config.table)
        query = self._filter_tenant_uuid(query)
        return await self.call_filter_search.async_search_from_query(
            self.session, query, parameters
        )

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Callfilter]:
        """Find all Callfilter by criteria.

        Returns:
            list of Callfilter.

        """
        result: Sequence[Callfilter] = await super().find_all_by(criteria)
        return list(result)

    async def create(self, call_filter: Callfilter) -> Callfilter:
        """Create a new Callfilter.

        Args:
            call_filter: The call filter instance to create.

        Returns:
            The created Callfilter instance.

        """
        self._fill_default_values(call_filter)
        return await super().create(call_filter)

    def _fill_default_values(self, call_filter: Callfilter) -> None:
        """Fill default values for a new Callfilter.

        Args:
            call_filter: The Callfilter instance.

        """
        call_filter.type = "bosssecretary"

    async def associate_recipients(
        self, call_filter: Callfilter, recipients: list[Callfiltermember]
    ) -> None:
        """Associate a list of recipients with the call filter.

        Args:
            call_filter: The Callfilter instance.
            recipients: The list of Callfiltermember instances.

        """
        for recipient in recipients:
            self._fill_default_recipient_values(recipient)
        call_filter.recipients = recipients
        await self.session.flush()

    def _fill_default_recipient_values(self, recipient: Callfiltermember) -> None:
        """Fill default values for a recipient.

        Args:
            recipient: The Callfiltermember instance.

        """
        recipient.type = "user"
        recipient.bstype = "boss"

    async def associate_surrogates(
        self, call_filter: Callfilter, surrogates: list[Callfiltermember]
    ) -> None:
        """Associate a list of surrogates with the call filter.

        Args:
            call_filter: The Callfilter instance.
            surrogates: The list of Callfiltermember instances.

        """
        for surrogate in surrogates:
            self._fill_default_surrogate_values(surrogate)
        call_filter.surrogates = surrogates
        await self.session.flush()

    def _fill_default_surrogate_values(self, surrogate: Callfiltermember) -> None:
        """Fill default values for a surrogate.

        Args:
            surrogate: The Callfiltermember instance.

        """
        surrogate.type = "user"
        surrogate.bstype = "secretary"

    async def update_fallbacks(
        self, call_filter: Callfilter, fallbacks: dict[str, Dialaction]
    ) -> None:
        """Update the fallback dialactions for the call filter.

        Args:
            call_filter: The Callfilter instance.
            fallbacks: The new fallback actions.

        """
        for event in list(call_filter.callfilter_dialactions.keys()):
            if event not in fallbacks:
                del call_filter.callfilter_dialactions[event]

        for event, dialaction in fallbacks.items():
            if dialaction is None:
                call_filter.callfilter_dialactions.pop(event, None)
                continue

            if event not in call_filter.callfilter_dialactions:
                dialaction.event = event
                dialaction.category = "callfilter"
                call_filter.callfilter_dialactions[event] = dialaction  # type: ignore
            else:
                call_filter.callfilter_dialactions[event].action = dialaction.action
                call_filter.callfilter_dialactions[
                    event
                ].actionarg1 = dialaction.actionarg1
                call_filter.callfilter_dialactions[
                    event
                ].actionarg2 = dialaction.actionarg2

        await self.session.flush()

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.

        """
        if self.tenant_uuids is not None:
            query = query.filter(Callfilter.tenant_uuid.in_(self.tenant_uuids))
        return query
