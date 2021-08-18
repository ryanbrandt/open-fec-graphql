from typing import TypedDict


class FecElectioneeringAggregatesDict(TypedDict):
    candidate: str
    candidate_id: str
    candidate_name: str
    committee: str
    committee_id: str
    committee_name: str
    count: int
    cycle: int
    total: int
