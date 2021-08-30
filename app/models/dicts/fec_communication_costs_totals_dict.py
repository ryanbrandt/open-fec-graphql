from typing import TypedDict


class FecCommunicationCostsTotalsDict(TypedDict):
    candidate_id: str
    cycle: int
    support_oppose_indicator: str
    total: int
