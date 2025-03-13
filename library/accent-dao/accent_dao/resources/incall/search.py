# Copyright 2025 Accent Communications

from sqlalchemy import String, and_, cast, func, select

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.incall import Incall
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class IncallSearchSystem(SearchSystem):
    """Search system for InCall, adds search on extension."""

    def search_from_query(self, query, parameters=None):
        """Perform search using extra filters for the incall model."""
        if (
            exten_param := parameters.pop("exten", None)
            if isinstance(parameters, dict)
            else None
        ):
            query = self._filter_exact_match_exten(query, exten_param)
        return super().search_from_query(query, parameters)

    def _filter_exact_match_exten(self, query, exten):
        return (
            query.join(
                Dialaction,
                and_(
                    Dialaction.action == "incall",
                    Dialaction.actionarg1 == cast(Incall.id, String),
                ),
            )
            .join(
                Extension,
                and_(
                    Extension.type == "incall",
                    Extension.typeval == cast(Incall.id, String),
                ),
            )
            .filter(Extension.exten.ilike(f"%{exten}%"))
        )


config = SearchConfig(
    table=Incall,
    columns={
        "id": Incall.id,
        "description": Incall.description,
        "preprocess_subroutine": Incall.preprocess_subroutine,
        "exten": Extension.exten,
        "user_id": Incall.user_id,
    },
    search={
        "description": Incall.description,
        "preprocess_subroutine": Incall.preprocess_subroutine,
        "exten": Extension.exten,
    },
    default_sort="id",
)

incall_search = IncallSearchSystem(config)
