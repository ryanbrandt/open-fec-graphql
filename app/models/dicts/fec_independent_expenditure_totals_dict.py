from typing import TypedDict


class FecIndependentExpenditureTotalsDict(TypedDict):
    candidate_id: str
    cycle: int
    support_oppose_indicator: str
    total: int
