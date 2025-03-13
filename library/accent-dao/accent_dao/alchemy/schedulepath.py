# file: accent_dao/alchemy/schedulepath.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .groupfeatures import GroupFeatures
    from .incall import Incall
    from .outcall import Outcall
    from .queuefeatures import QueueFeatures
    from .schedule import Schedule
    from .userfeatures import UserFeatures


class SchedulePath(Base):
    """Represents a path within a schedule.

    Attributes:
        schedule_id: The ID of the associated schedule.
        path: The type of path ('user', 'group', 'queue', 'incall',
            'outcall', 'voicemenu').
        pathid: The ID of the entity associated with the path.
        incall: Relationship to Incall (if path is 'incall').
        group: Relationship to GroupFeatures (if path is 'group').
        outcall: Relationship to Outcall (if path is 'outcall').
        queue: Relationship to QueueFeatures (if path is 'queue').
        user: Relationship to UserFeatures (if path is 'user').
        schedule: Relationship to Schedule.

    """

    __tablename__: str = "schedule_path"
    __table_args__: tuple = (
        PrimaryKeyConstraint("schedule_id", "path", "pathid"),
        Index("schedule_path_path", "path", "pathid"),
        Index("schedule_path__idx__schedule_id", "schedule_id"),
    )

    schedule_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("schedule.id", ondelete="CASCADE"), primary_key=True
    )
    path: Mapped[str] = mapped_column(
        String, nullable=False, primary_key=True
    )  # Use String
    pathid: Mapped[int] = mapped_column(
        Integer, autoincrement=False, primary_key=True
    )  # No autoincrement

    incall: Mapped["Incall"] = relationship(
        "Incall",
        primaryjoin="""and_(
            SchedulePath.path == 'incall',
            SchedulePath.pathid == Incall.id
        )""",
        foreign_keys="SchedulePath.pathid",
        viewonly=True,
    )
    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            SchedulePath.path == 'group',
            SchedulePath.pathid == GroupFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        viewonly=True,
    )
    outcall: Mapped["Outcall"] = relationship(
        "Outcall",
        primaryjoin="""and_(
            SchedulePath.path == 'outcall',
            SchedulePath.pathid == Outcall.id
        )""",
        foreign_keys="SchedulePath.pathid",
        viewonly=True,
    )
    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            SchedulePath.path == 'queue',
            SchedulePath.pathid == QueueFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        viewonly=True,
    )
    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            SchedulePath.path == 'user',
            SchedulePath.pathid == UserFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        viewonly=True,
    )
    schedule: Mapped["Schedule"] = relationship("Schedule")
