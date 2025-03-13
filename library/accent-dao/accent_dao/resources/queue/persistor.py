# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.schedulepath import SchedulePath
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.queuemember import QueueMember
    from accent_dao.alchemy.schedule import Schedule


class QueuePersistor(CriteriaBuilderMixin, AsyncBasePersistor[QueueFeatures]):
    """Persistor class for QueueFeatures model."""

    _search_table = QueueFeatures

    def __init__(
        self,
        session: AsyncSession,
        queue_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize QueuePersistor.

        Args:
            session: Async database session.
            queue_search: Search system for queues.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = queue_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find queues based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(QueueFeatures)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> QueueFeatures:
        """Retrieve a single queue by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            QueueFeatures: The found queue.

        Raises:
            NotFoundError: If no queue is found.

        """
        queue = await self.find_by(criteria)
        if not queue:
            raise errors.NotFoundError("Queue", **criteria)
        return queue

    async def find_all_by(self, criteria: dict[str, Any]) -> list[QueueFeatures]:
        """Find all QueueFeatures by criteria.

        Returns:
            list of QueueFeatures.

        """
        result: Sequence[QueueFeatures] = await super().find_all_by(criteria)
        return list(result)

    async def associate_schedule(
        self, queue: QueueFeatures, schedule: "Schedule"
    ) -> None:
        """Associate a schedule with a queue.

        Args:
            queue: The queue object.
            schedule: The schedule object.

        """
        for path in queue.schedule_paths:
            if path.schedule_id == schedule.id:
                return

        schedule_path = SchedulePath(
            path="queue", schedule_id=schedule.id, pathid=queue.id, schedule=schedule
        )
        queue.schedule_paths.append(schedule_path)
        await self.session.flush()

    async def dissociate_schedule(
        self, queue: QueueFeatures, schedule: "Schedule"
    ) -> None:
        """Dissociate a schedule from a queue.

        Args:
            queue: The queue object.
            schedule: The schedule object.

        """
        for path in queue.schedule_paths:
            if path.schedule_id == schedule.id:
                queue.schedule_paths.remove(path)
                break
        await self.session.flush()

    async def associate_member_user(
        self, queue: QueueFeatures, member: "QueueMember"
    ) -> None:
        """Associate a user member with a queue.

        Args:
            queue: The queue object.
            member: The user member object to associate.

        """
        for existing_member in queue.user_queue_members:
            if existing_member.userid == member.userid:
                return

        self._fill_user_queue_member_default_values(member)
        queue.user_queue_members.append(member)
        await self.session.flush()

    def _fill_user_queue_member_default_values(self, member: "QueueMember") -> None:
        """Fill the default values for the membership.

        Args:
            member: queue member to set default

        """
        member.category = "queue"
        member.usertype = "user"

    async def dissociate_member_user(
        self, queue: QueueFeatures, member: "QueueMember"
    ) -> None:
        """Dissociate a user member from a queue.

        Args:
            queue: The queue object.
            member: The user member object to dissociate.

        """
        if member in queue.user_queue_members:
            queue.user_queue_members.remove(member)
            await self.session.flush()

    async def associate_member_agent(
        self, queue: QueueFeatures, member: "QueueMember"
    ) -> None:
        """Associate an agent member with a queue.

        Args:
            queue: The queue object.
            member: The agent member object to associate.

        """
        for existing_member in queue.agent_queue_members:
            if existing_member.userid == member.userid:
                return

        self._fill_agent_queue_member_default_values(member)
        queue.agent_queue_members.append(member)
        await self.session.flush()

    def _fill_agent_queue_member_default_values(self, member: "QueueMember") -> None:
        """Fill in default values for agent queue members.

        Args:
            member: The queue member object.

        """
        member.category = "queue"
        member.usertype = "agent"

    async def dissociate_member_agent(
        self, queue: QueueFeatures, member: "QueueMember"
    ) -> None:
        """Dissociate an agent member from a queue.

        Args:
            queue: The queue object.
            member: The agent member object to dissociate.

        """
        if member in queue.agent_queue_members:
            queue.agent_queue_members.remove(member)
            await self.session.flush()
