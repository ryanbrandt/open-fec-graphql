import graphene
from typing import Union

from app.models.graphql.filters.committee_graphql_filter import CommitteeGraphQLFilter
from app.models.graphql.graphql_committee import GraphQLCommittee
from app.models.graphql.collections.graphql_committee_collection import GraphQLCommitteeCollection
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.utils.api import FecApi
from app.utils.setup_logger import get_logger
from app.cache.cached_query import cached_query


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    comittee = graphene.Field(
        GraphQLCommittee, id=graphene.String(required=True))
    committee_collection = graphene.Field(
        GraphQLCommitteeCollection, where=graphene.Argument(CommitteeGraphQLFilter, required=False))

    @cached_query
    async def resolve_committee(self, info, id) -> Union[GraphQLCommittee, None]:
        result = await FecApi.get(f'/committee/{id}', FecCommitteeDict)

        if result.pagination['count'] > 0:
            committee = result.results[0]

            return GraphQLCommittee(committee)

        return None

    @cached_query
    async def resolve_committee_collection(self, info, where: Union[CommitteeGraphQLFilter, None] = None) -> GraphQLCommitteeCollection:
        results = await FecApi.get('/committees', FecCommitteeDict, params=where.build_api_filter_dict() if where else {})

        return GraphQLCommitteeCollection(results.results, pagination=results.pagination)
