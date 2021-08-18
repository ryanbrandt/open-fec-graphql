from typing import TypedDict, List


class FecElectioneeringAggregatesSearchFilterDict(TypedDict):
    candidate_id: List[str]
    comittee_id: List[str]
    cycle: List[int]
