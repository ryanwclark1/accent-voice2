# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from accent_dao.alchemy.conference import Conference
    from accent_dao.alchemy.groupfeatures import GroupFeatures
    from accent_dao.alchemy.incall import Incall
    from accent_dao.alchemy.parking_lot import ParkingLot
    from accent_dao.alchemy.queuefeatures import QueueFeatures


class ExtensionPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Extension]):
    """Persistor class for Extension model."""

    _search_table = Extension

    def __init__(
        self,
        session: AsyncSession,
        extension_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ExtensionPersistor.

        Args:
            session: Async database session.
            extension_search: Search system for extensions.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = extension_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find extensions based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Extension)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching extensions."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Extension:
        """Retrieve a single extension by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Extension: The found extension.

        Raises:
            NotFoundError: If no extension is found.

        """
        extension = await self.find_by(criteria)
        if not extension:
            raise errors.NotFoundError("Extension", **criteria)
        return extension

    async def associate_incall(self, incall: "Incall", extension: "Extension") -> None:
        """Associate an incall with an extension.

        Args:
            incall: The incall object.
            extension: The extension object.

        """
        extension.type = "incall"
        extension.typeval = str(incall.id)
        await self.session.flush()

    async def dissociate_incall(self, incall: "Incall", extension: "Extension") -> None:
        """Dissociate an incall from an extension.

        Args:
            incall: The incall object.
            extension: The extension object.

        """
        if incall is extension.incall:
            extension.type = "user"
            extension.typeval = "0"
            await self.session.flush()

    async def associate_group(
        self, group: "GroupFeatures", extension: "Extension"
    ) -> None:
        """Associate a group with an extension.

        Args:
            group: The group object.
            extension: The extension object.

        """
        extension.type = "group"
        extension.typeval = str(group.id)
        await self.session.flush()

    async def dissociate_group(
        self, group: "GroupFeatures", extension: "Extension"
    ) -> None:
        """Dissociate a group from an extension.

        Args:
            group: The group object.
            extension: The extension object.

        """
        if group is extension.group:
            extension.type = "user"
            extension.typeval = "0"
            await self.session.flush()

    async def associate_queue(
        self, queue: "QueueFeatures", extension: "Extension"
    ) -> None:
        """Associate a queue with an extension.

        Args:
            queue: The queue object.
            extension: The extension object.

        """
        extension.type = "queue"
        extension.typeval = str(queue.id)
        await self.session.flush()

    async def dissociate_queue(
        self, queue: "QueueFeatures", extension: "Extension"
    ) -> None:
        """Dissociate a queue from an extension.

        Args:
            queue: The queue object.
            extension: The extension object.

        """
        if queue is extension.queue:
            extension.type = "user"
            extension.typeval = "0"
            await self.session.flush()

    async def associate_conference(
        self, conference: "Conference", extension: "Extension"
    ) -> None:
        """Associate a conference with an extension.

        Args:
            conference: The conference object.
            extension: The extension object.

        """
        extension.type = "conference"
        extension.typeval = str(conference.id)
        await self.session.flush()

    async def dissociate_conference(
        self, conference: "Conference", extension: "Extension"
    ) -> None:
        """Dissociate a conference from an extension.

        Args:
            conference: The conference object.
            extension: The extension object.

        """
        if conference is extension.conference:
            extension.type = "user"
            extension.typeval = "0"
            await self.session.flush()

    async def associate_parking_lot(
        self, parking_lot: "ParkingLot", extension: "Extension"
    ) -> None:
        """Associate a parking lot with an extension.

        Args:
            parking_lot: The parking lot object.
            extension: The extension object.

        """
        extension.type = "parking"
        extension.typeval = str(parking_lot.id)
        await self.session.flush()

    async def dissociate_parking_lot(
        self, parking_lot: "ParkingLot", extension: "Extension"
    ) -> None:
        """Dissociate a parking lot from an extension.

        Args:
            parking_lot: The parking lot object.
            extension: The extension object.

        """
        if parking_lot is extension.parking_lot:
            extension.type = "user"
            extension.typeval = "0"
            await self.session.flush()
