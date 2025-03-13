# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticiax import StaticIAX as RegisterIAX
from accent_dao.alchemy.trunkfeatures import TrunkFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class RegisterIAXPersistor(CriteriaBuilderMixin, AsyncBasePersistor[RegisterIAX]):
    """Persistor class for RegisterIAX model."""

    _search_table = RegisterIAX

    def __init__(self, session: AsyncSession, register_iax_search: Any) -> None:
        """Initialize RegisterIAXPersistor.

        Args:
            session: Async database session.
            register_iax_search: Search system for register_iax entries.

        """
        super().__init__(session, self._search_table)
        self.search_system = register_iax_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find register_iax entries based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(RegisterIAX).where(RegisterIAX.var_name == "register")
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> RegisterIAX:
        """Retrieve a single register_iax entry by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            RegisterIAX: The found register_iax entry.

        Raises:
            NotFoundError: If no register_iax entry is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("RegisterIAX", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[RegisterIAX]:
        """Find all RegisterIAX by criteria.

        Returns:
            list of RegisterIAX.

        """
        result: Sequence[RegisterIAX] = await super().find_all_by(criteria)
        return list(result)

    async def delete(self, register_iax: RegisterIAX) -> None:
        """Delete register entry and update associated trunk if needed.

        Args:
            register_iax: RegisterIAX object

        """
        trunk = (
            await self.session.execute(
                select(TrunkFeatures).filter(
                    TrunkFeatures.register_iax_id == register_iax.id
                )
            )
        ).scalar_one_or_none()
        if trunk:
            trunk.registercommented = 0

        await super().delete(register_iax)
