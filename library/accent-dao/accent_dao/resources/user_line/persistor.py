from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from collections.abc import Sequence



class UserLinePersistor(CriteriaBuilderMixin, AsyncBasePersistor[UserLine]):
    """Persistor class for UserLine model."""

    _search_table = UserLine

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserLinePersistor.

        Args:
            session: Database session.

        """
        super().__init__(session, self._search_table)
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find user lines based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(UserLine)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> UserLine:
        """Retrieve a single user line by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            UserLine: The found user line.

        Raises:
            NotFoundError: If no user line is found.

        """
        user_line = await self.find_by(criteria)
        if not user_line:
            raise errors.NotFoundError("UserLine", **criteria)
        return user_line

    async def find_all_by(self, **criteria: dict) -> list[UserLine]:
        """Find all UserLine by criteria.

        Returns:
            list of UserLine.

        """
        result: Sequence[UserLine] = await super().find_all_by(criteria)
        return list(result)

    async def associate_user_line(
        self, user: UserFeatures, line: LineFeatures
    ) -> UserLine:
        """Associate a user with a line.

        If a UserLine already exists for the given user and line, it is returned.
        Otherwise, a new UserLine is created, associating the user with the line.
        The main_user and main_line flags are set based on whether existing associations
        are present.

        Args:
            user: The UserFeatures object.
            line: The LineFeatures object.

        Returns:
            The existing or newly created UserLine object.

        """
        user_line = await self.find_by(user_id=user.id, line_id=line.id)
        if user_line:
            return user_line

        main_user_line = await self.find_by(main_user=True, line_id=line.id)
        user_main_line = await self.find_by(main_line=True, user_id=user.id)

        user_line = UserLine(
            user_id=user.id,
            line_id=line.id,
            main_line=False if user_main_line else True,
            main_user=False if main_user_line else True,
        )

        self.session.add(user_line)
        await self.session.flush()

        return user_line

    async def dissociate_user_line(
        self, user: UserFeatures, line: LineFeatures
    ) -> UserLine | None:
        """Dissociate a user from a line.

        If a UserLine exists for the given user and line, it is deleted.
        If the UserLine represents the main line for the user,
        the oldest remaining line is set as the main line.

        Args:
            user: The UserFeatures object.
            line: The LineFeatures object.

        """
        user_line = await self.find_by(user_id=user.id, line_id=line.id)
        if not user_line:
            return None

        if user_line.main_line:
            await self._set_oldest_main_line(user)

        await self.session.delete(user_line)
        await self.session.flush()

        return user_line

    async def _set_oldest_main_line(self, user: UserFeatures) -> None:
        """Set the oldest remaining line as the main line for the user.

        Args:
            user: The UserFeatures object.

        """
        oldest_user_line = (
            await self.session.execute(
                select(UserLine)
                .filter(UserLine.user_id == user.id)
                .filter(UserLine.main_line.is_(False))
                .order_by(UserLine.line_id.asc())
            )
        ).scalar_one_or_none()

        if oldest_user_line:
            oldest_user_line.main_line = True
            await self.session.flush()

    async def associate_all_lines(
        self, user: UserFeatures, lines: list[LineFeatures]
    ) -> list[UserLine]:
        """Associate all provided lines with a user.

        This method ensures that each provided line is associated with the user.
        It marks the first line as the main line if no existing main line is found.

        Args:
            user: The UserFeatures object.
            lines: A list of LineFeatures objects to associate.

        Returns:
            A list of created or existing UserLine objects.

        """
        new_user_lines: list[UserLine] = []
        main_line_set = False

        for line in lines:
            user_line = await self.find_by(user_id=user.id, line_id=line.id)
            if not user_line:
                is_main_line = not main_line_set
                user_line = UserLine(
                    user_id=user.id,
                    line_id=line.id,
                    main_line=is_main_line,
                    main_user=False,
                )
                self.session.add(user_line)
            else:
                # Update existing UserLine if it's already associated
                if not main_line_set:
                    user_line.main_line = True
                    main_line_set = True
                else:
                    user_line.main_line = False  # Ensure only one main line
            new_user_lines.append(user_line)
            main_line_set = main_line_set or user_line.main_line

        await self.session.flush()
        return new_user_lines
