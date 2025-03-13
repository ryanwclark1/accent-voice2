# file: accent_dao/alchemy/endpoint_sip_options_view.py  # noqa: ERA001
# Copyright 2025 Accent Communications
import logging

from sqlalchemy import (
    Index,
    String,
    Subquery,
    func,
    inspect,
    join,
    literal,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy_utils import create_materialized_view

from accent_dao.helpers.db_manager import Base, get_async_session, get_session

from .endpoint_sip import EndpointSIP, EndpointSIPTemplate
from .endpoint_sip_section import EndpointSIPSection
from .endpoint_sip_section_option import EndpointSIPSectionOption

logger = logging.getLogger(__name__)

def _generate_selectable() -> Subquery:
    """Generate the selectable for the materialized view."""
    cte = select(
        EndpointSIP.uuid.label("uuid"),
        literal(0).label("level"),
        literal("0", String).label("path"),
        EndpointSIP.uuid.label("root"),
    ).cte(recursive=True)

    endpoints = cte.union_all(
        select(
            EndpointSIPTemplate.parent_uuid.label("uuid"),
            (cte.c.level + 1).label("level"),
            (
                cte.c.path
                + func.cast(
                    func.row_number().over(
                        partition_by=cte.c.level,
                        order_by=EndpointSIPTemplate.priority,
                    ),
                    String,
                )
            ).label("path"),
            cte.c.root,
        ).select_from(
            join(cte, EndpointSIPTemplate, cte.c.uuid == EndpointSIPTemplate.child_uuid)
        )
    )

    return (
        select(
            endpoints.c.root,
            func.jsonb_object(
                func.array_agg(
                    aggregate_order_by(
                        EndpointSIPSectionOption.key,
                        endpoints.c.path.desc(),
                    )
                ),
                func.array_agg(
                    aggregate_order_by(
                        EndpointSIPSectionOption.value,
                        endpoints.c.path.desc(),
                    )
                ),
            ).label("options"),
        )
        .select_from(
            join(
                endpoints,
                EndpointSIPSection,
                EndpointSIPSection.endpoint_sip_uuid == endpoints.c.uuid,
            ).join(
                EndpointSIPSectionOption,
                EndpointSIPSectionOption.endpoint_sip_section_uuid
                == EndpointSIPSection.uuid,
            )
        )
        .group_by(endpoints.c.root)
        .subquery()  # Correctly creates a subquery
    )


class EndpointSIPOptionsView:
    """Provides a materialized view for combined SIP endpoint options.

    Taking into account inheritance from templates.
    """

    __view_dependencies__ = (EndpointSIPSectionOption, EndpointSIP)  # Kept

    @classmethod
    def create_view(cls, metadata: Base.metadata) -> None:  # type: ignore
        """Create the materialized view "endpoint_sip_options_view".

        Args:
            metadata: The metadata object from sqlalchemy

        """
        # Added a check to see if the view already exists.
        mat_view = create_materialized_view(
            "endpoint_sip_options_view",
            _generate_selectable(),
            metadata=metadata,
            indexes=[
                Index("endpoint_sip_options_view__idx_root", text("root"), unique=True),
            ],
        )
        # Added check to avoid dropping and recreating view.
        with metadata.bind.connect() as connection:  # type: ignore
            insp = inspect(connection)
            if "endpoint_sip_options_view" not in insp.get_view_names():
                mat_view.create(metadata.bind, checkfirst=True)  # type: ignore

    @classmethod
    def get_option_value(
        cls, options: dict[str, str], option: str
    ) -> str | None:  # Added Options
        """Retrieve the value of a specific option from the options dictionary.

        Args:
            options: options dictionary
            option: The name of the option.

        Returns:
            The value of the option, or None if the option is not found.

        """
        return options.get(option, None)

    @classmethod
    async def refresh(cls, concurrently: bool = True) -> None:
        """Asynchronously refresh the materialized view."""
        async with get_async_session() as session:
            if concurrently:
                await session.execute(
                    text(
                        "REFRESH MATERIALIZED VIEW CONCURRENTLY endpoint_sip_options_view"
                    )
                )
            else:
                await session.execute(
                    text("REFRESH MATERIALIZED VIEW endpoint_sip_options_view")
                )
            await session.commit()
            logger.info("Refreshed materialized view: endpoint_sip_options_view")

    @classmethod
    def refresh_sync(cls, concurrently: bool = True) -> None:
        """Refresh the materialized view synchronously."""
        with get_session() as session:
            if concurrently:
                session.execute(
                    text(
                        "REFRESH MATERIALIZED VIEW CONCURRENTLY endpoint_sip_options_view"
                    )
                )
            else:
                session.execute(
                    text("REFRESH MATERIALIZED VIEW endpoint_sip_options_view")
                )

            session.commit()
            logger.info("Refreshed materialized view: endpoint_sip_options_view")
