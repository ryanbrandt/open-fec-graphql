import graphene
from typing import Union

from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.graphql.graphql_candidate import GraphQLCandidate
from app.models.graphql.graphql_candidate_collection import GraphQLCandidateCollection
from app.models.graphql.candidate_graphql_filter import CandidateGraphQLFilter
from app.utils.setup_logger import get_logger
from app.utils.api import FecApi


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    candidate = graphene.Field(GraphQLCandidate, id=graphene.String(
        required=True))
    candidate_collection = graphene.Field(
        GraphQLCandidateCollection, where=graphene.Argument(
            CandidateGraphQLFilter, required=False)
    )

    async def resolve_candidate(self, info, id) -> Union[GraphQLCandidate, None]:
        result = await FecApi.get(f'/candidate/{id}', FecCandidateDict)

        if len(result.results) > 0:
            candidate = result.results[0]

            return GraphQLCandidate(candidate)

        return None

    async def resolve_candidate_collection(self, info, where: Union[CandidateGraphQLFilter, None] = None) -> GraphQLCandidateCollection:
        result = await FecApi.get(f'/candidates/search', FecCandidateDict, params=where.build_api_filter_dict() if where else {})

        return GraphQLCandidateCollection(result.results, pagination=result.pagination)
