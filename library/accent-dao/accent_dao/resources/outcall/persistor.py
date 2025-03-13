# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.dialpattern import DialPattern
from accent_dao.alchemy.outcall import Outcall
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence
    from accent_dao.alchemy.extension import Extension
    from accent_dao.alchemy.rightcall import RightCall


class OutcallPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Outcall]):
    """Persistor class for Outcall model."""

    _search_table = Outcall

    def __init__(
        self,
        session: AsyncSession,
        outcall_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize OutcallPersistor.

        Args:
            session: Async database session.
            outcall_search: Search system for outcalls.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = outcall_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find outcalls based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Outcall)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Outcall:
        """Retrieve a single outcall by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Outcall: The found outcall.

        Raises:
            NotFoundError: If no outcall is found.

        """
        outcall = await self.find_by(criteria)
        if not outcall:
            raise errors.NotFoundError("Outcall", **criteria)
        return outcall

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Outcall]:
        """Find all Outcall by criteria.

        Returns:
            list of Outcall.

        """
        result: Sequence[Outcall] = await super().find_all_by(criteria)
        return list(result)

    async def associate_call_permission(
        self, outcall: Outcall, call_permission: "RightCall"
    ) -> None:
        """Associate a call permission with an outcall.

        Args:
            outcall: The outcall object.
            call_permission: The call permission object.

        """
        if call_permission not in outcall.call_permissions:
            outcall.call_permissions.append(call_permission)
            await self.session.flush()

    async def dissociate_call_permission(
        self, outcall: Outcall, call_permission: "RightCall"
    ) -> None:
        """Dissociate a call permission from an outcall.

        Args:
            outcall: The outcall object.
            call_permission: The call permission object.

        """
        if call_permission in outcall.call_permissions:
            outcall.call_permissions.remove(call_permission)
            await self.session.flush()

    async def associate_extension(
        self, outcall: Outcall, extension: "Extension", **kwargs: Any
    ) -> None:
        """Associate an extension with an outcall.

        Args:
            outcall: The outcall object.
            extension: The extension object.
            **kwargs: Keyword arguments for dial pattern attributes.

        """
        if extension not in outcall.extensions:
            extension.type = "outcall"
            dialpattern = DialPattern(
                type="outcall", typeid=outcall.id, exten=extension.exten, **kwargs
            )
            outcall.dialpatterns.append(dialpattern)
            # Use list comprehension for a more concise way
            index = [
                i for i, dp in enumerate(outcall.dialpatterns) if dp == dialpattern
            ][0]
            outcall.dialpatterns[index].extension = extension
            outcall._fix_context()
            await self.session.flush()

    async def dissociate_extension(
        self, outcall: Outcall, extension: "Extension"
    ) -> None:
        """Dissociate an extension from an outcall.

        Args:
            outcall: The outcall object.
            extension: The extension object.

        """
        if extension in outcall.extensions:
            outcall.extensions.remove(extension)
            extension.type = "user"
            extension.typeval = "0"
            outcall._fix_context()
            await self.session.flush()

    async def update_extension_association(
        self, outcall: Outcall, extension: "Extension", **kwargs: Any
    ) -> None:
        """Update the association between an outcall and an extension.

        Args:
            outcall: The outcall object.
            extension: The extension object.
            **kwargs: Keyword arguments for dial pattern attributes.

        """
        for dialpattern in outcall.dialpatterns:
            if extension == dialpattern.extension:
                for key, value in kwargs.items():
                    setattr(dialpattern, key, value)
                await self.session.flush()
