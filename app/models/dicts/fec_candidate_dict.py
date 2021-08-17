from typing import TypedDict


class FecCandidateDict(TypedDict):
    candidate_id: str
    name: str
    office: str
    state: str
    election_years: list[str]
    address_city: str
    address_state: str
    district: str
    district_number: int
    office_full: str
    party_full: str
