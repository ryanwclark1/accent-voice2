# file: accent_dao/models/stats_conf.py
# Copyright 2025 Accent Communications

from sqlalchemy import (
    Index,
    Integer,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class StatsConf(Base):
    """Represents statistics configuration settings.

    Attributes:
        id: The unique identifier for the statistics configuration.
        name: The name of the configuration.
        hour_start: The starting hour for statistics collection.
        hour_end: The ending hour for statistics collection.
        homepage:  (Unclear purpose).
        timezone: The timezone for statistics collection.
        default_delta: The default delta.
        monday: Flag (0 or 1) indicating if statistics are collected on Monday.
        tuesday: Flag (0 or 1) indicating if statistics are collected on Tuesday.
        wednesday: Flag (0 or 1) indicating if statistics are collected on Wednesday.
        thursday: Flag (0 or 1) indicating if statistics are collected on Thursday.
        friday: Flag (0 or 1) indicating if statistics are collected on Friday.
        saturday: Flag (0 or 1) indicating if statistics are collected on Saturday.
        sunday: Flag (0 or 1) indicating if statistics are collected on Sunday.
        period1:  (Purpose unclear).
        period2:  (Purpose unclear).
        period3:  (Purpose unclear).
        period4:  (Purpose unclear).
        period5:  (Purpose unclear).
        dbegcache:  (Purpose unclear).
        dendcache:  (Purpose unclear).
        dgenercache:  (Purpose unclear).
        dcreate:  (Purpose unclear).
        dupdate:  (Purpose unclear).
        disable: Flag (0 or 1) indicating if statistics collection is disabled.
        description: A description of the statistics configuration.

    """

    __tablename__: str = "stats_conf"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
        Index("stats_conf__idx__disable", "disable"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, server_default="")
    hour_start: Mapped[str] = mapped_column(Time, nullable=False)
    hour_end: Mapped[str] = mapped_column(Time, nullable=False)
    homepage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timezone: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    default_delta: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default="0"
    )

    monday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    tuesday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    wednesday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    thursday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    friday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    saturday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )
    sunday: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )

    period1: Mapped[str] = mapped_column(String(16), nullable=False, server_default="0")
    period2: Mapped[str] = mapped_column(String(16), nullable=False, server_default="0")
    period3: Mapped[str] = mapped_column(String(16), nullable=False, server_default="0")
    period4: Mapped[str] = mapped_column(String(16), nullable=False, server_default="0")
    period5: Mapped[str] = mapped_column(String(16), nullable=False, server_default="0")

    dbegcache: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    dendcache: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    dgenercache: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    dcreate: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    dupdate: Mapped[int | None] = mapped_column(
        Integer, server_default="0", nullable=True
    )
    disable: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default=text("0")
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
