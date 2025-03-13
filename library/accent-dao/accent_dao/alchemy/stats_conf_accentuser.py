# file: accent_dao/alchemy/stats_conf_accentuser.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class StatsConfAccentUser(Base):
    """Represents the association between StatsConf and Accent users.

    Attributes:
        stats_conf_id: The ID of the associated StatsConf.
        user_id: The ID of the associated user.

    """

    __tablename__: str = "stats_conf_accentuser"
    __table_args__: tuple = (PrimaryKeyConstraint("stats_conf_id", "user_id"),)

    stats_conf_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
