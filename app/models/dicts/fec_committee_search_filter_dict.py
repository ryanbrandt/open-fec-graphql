from typing import TypedDict


class FecCommitteeSearchFilterDict(TypedDict):
    committee_id: list[str]
    candidate_id: list[str]
    cycle: list[int]
    party: list[str]
