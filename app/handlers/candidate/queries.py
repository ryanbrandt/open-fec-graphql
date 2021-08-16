import graphene
from typing import List, Union

from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.candidate import Candidate
from app.utils.setup_logger import get_logger
from app.utils.api import FecApi
from app.models.candidate import Candidate


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    candidate = graphene.Field(Candidate, id=graphene.String(
        required=True))
    candidate_collection = graphene.List(Candidate)

    async def resolve_candidate(self, info, id) -> Union[Candidate, None]:
        result = await FecApi.get(f'/candidate/{id}', FecCandidateDict)

        if len(result.results) > 0:
            candidate = result.results[0]

            return Candidate(candidate)

        return None

    async def resolve_candidate_collection(self, info) -> List[Candidate]:
        result = await FecApi.get(f'/candidates', FecCandidateDict)

        if len(result.results) > 0:
            return [Candidate(candidate) for candidate in result.results]

        return []
