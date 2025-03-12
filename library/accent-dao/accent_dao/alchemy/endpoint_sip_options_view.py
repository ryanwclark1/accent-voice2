# file: accent_dao/models/endpoint_sip_options_view.py
# Copyright 2025 Accent Communications

# TODO: Update materialized view
from typing import Any

from sqlalchemy import Index, String, func, join, literal, select, text
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy.orm import Mapped

# Removed, as we are handling view creation differently: from sqlalchemy_utils import create_materialized_view
from accent_dao.helpers.db_manager import Base

from .endpoint_sip import EndpointSIP, EndpointSIPTemplate
from .endpoint_sip_section import EndpointSIPSection
from .endpoint_sip_section_option import EndpointSIPSectionOption


def _generate_selectable() -> Any:  # Added Any Type
    """Generates the selectable for the materialized view."""
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
                        partition_by="level",
                        order_by=EndpointSIPTemplate.priority,
                    ),
                    String,
                )
            ).label("path"),
            (cte.c.root),
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
        .subquery()  # Added Subquery Here
    )


# We can't inherit from MaterializedView if we are using the declarative base.
# class EndpointSIPOptionsView(MaterializedView):
# Instead, we create a regular class to hold the materialized view creation logic
class EndpointSIPOptionsView:
    """Provides a materialized view for combined SIP endpoint options,
    taking into account inheritance from templates.
    """

    # __table__ = create_materialized_view(  # Removed __table__ and moved it to a function
    #     "endpoint_sip_options_view",
    #     _generate_selectable(),
    #     metadata=Base.metadata,
    #     indexes=[
    #         Index("endpoint_sip_options_view__idx_root", text("root"), unique=True),
    #     ],
    # )
    __view_dependencies__ = (EndpointSIPSectionOption, EndpointSIP)  # Kept

    @classmethod
    def create_view(cls, metadata: Base.metadata) -> None:  # type: ignore
        """Creates the materialized view "endpoint_sip_options_view".

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
        if "endpoint_sip_options_view" not in metadata.tables:
            mat_view.create(metadata.bind, checkfirst=True)

    @classmethod
    def get_option_value(
        cls, options: Mapped[dict[str, str]], option: str
    ) -> str | None:  # Added Options
        """Gets the value of a specific option from the options dictionary.

        Args:
            option: The name of the option.

        Returns:
            The value of the option, or None if the option is not found.

        """
        return options.get(option, None)
