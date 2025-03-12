# file: accent_dao/models/stats_conf_queue.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, PrimaryKeyConstraint, SmallInteger, text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class StatsConfQueue(Base):
    """Represents the association between StatsConf and queues.

    Attributes:
        stats_conf_id: The ID of the associated StatsConf.
        queuefeatures_id: The ID of the associated QueueFeatures.
        qos: The Quality of Service (QoS) setting.

    """

    __tablename__: str = "stats_conf_queue"
    __table_args__: tuple = (PrimaryKeyConstraint("stats_conf_id", "queuefeatures_id"),)

    stats_conf_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    queuefeatures_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    qos: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
