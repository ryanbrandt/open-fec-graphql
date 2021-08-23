from typing import TypedDict


class FecCommitteeDict(TypedDict):
    candidate_ids: list[str]
    committee_id: str
    comittee_type: str
    comittee_type_full: str
    cycles: list[int]
    party: str
    party_full: str
    name: str
    state: str
