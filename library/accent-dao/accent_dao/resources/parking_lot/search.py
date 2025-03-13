# Copyright 2025 Accent Communications

from sqlalchemy import String, func

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class ParkingLotSearchSystem(SearchSystem):
    """Search system for ParkingLot, adds search on extension."""

    def search_from_query(self, query, parameters=None):
        """Apply extension filter then do search from query"""
        if exten_param := (
            parameters.pop("exten", None) if isinstance(parameters, dict) else None
        ):
            query = self._filter_exact_match_exten(query, exten_param)
        return super().search_from_query(query, parameters)

    def _filter_exact_match_exten(self, query, exten):
        subquery = (
            select(Extension.typeval)
            .where(Extension.type == "parking")
            .where(Extension.exten.ilike(f"%{exten}%"))
            .scalar_subquery()
        )
        query = query.filter(func.cast(ParkingLot.id, String).in_(subquery))
        return query


config = SearchConfig(
    table=ParkingLot,
    columns={
        "id": ParkingLot.id,
        "name": ParkingLot.name,
        "slots_start": ParkingLot.slots_start,
        "slots_end": ParkingLot.slots_end,
        "timeout": ParkingLot.timeout,
        "exten": ParkingLot.exten,
        "context": ParkingLot.context,
    },
    search=["name", "slots_start", "slots_end", "timeout", "exten", "context"],
    default_sort="name",
)

parking_lot_search = ParkingLotSearchSystem(config)
