from typing import TypedDict, List


class FecCandidateSearchFilterDict(TypedDict):
    candidate_id: List[str]
    party: str
    office: str
    q: str
