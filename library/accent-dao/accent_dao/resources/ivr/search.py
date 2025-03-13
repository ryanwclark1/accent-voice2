# Copyright 2025 Accent Communications

from sqlalchemy import String, and_, cast, select
from sqlalchemy.orm import column_property

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.incall import Incall
from accent_dao.alchemy.ivr import IVR
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class IVRSearchSystem(SearchSystem):
    """Search system for IVR, adds search on extension."""

    def search_from_query(self, query, parameters=None):
        if exten_param := (
            parameters.pop("exten", None) if isinstance(parameters, dict) else None
        ):
            query = self._filter_exact_match_exten(query, exten_param)
        return super().search_from_query(query, parameters)

    def _filter_exact_match_exten(self, query, exten):
        return (
            query.join(
                Dialaction,
                and_(
                    Dialaction.action == "ivr",
                    Dialaction.actionarg1 == cast(IVR.id, String),
                ),
            )
            .join(
                Incall,
                and_(
                    Dialaction.category == "incall",
                    Dialaction.categoryval == cast(Incall.id, String),
                    Incall.commented == 0,
                ),
            )
            .filter(Incall.exten.ilike(f"%{exten}%"))
        )


config = SearchConfig(
    table=IVR,
    columns={
        "id": IVR.id,
        "name": IVR.name,
        "description": IVR.description,
        "exten": Incall.exten,
    },
    search=["id", "name", "description", "exten"],
    default_sort="name",
)


# Use the custom search system that supports extension searching
ivr_search = IVRSearchSystem(config)
