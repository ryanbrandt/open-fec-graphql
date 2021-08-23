from typing import Union
from app.models.graphql.filters.electioneering_aggregates_graphql_filter import ElectioneeringAggregatesGraphQLFilter
import graphene

from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict
from app.models.graphql.graphql_electioneering_aggregates_collection import GraphQLElectioneeringAggregatesCollection
from app.utils.setup_logger import get_logger
from app.utils.api import FecApi
from app.cache.cached_query import cached_query


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    electioneering_aggregates_collection = graphene.Field(
        GraphQLElectioneeringAggregatesCollection, where=graphene.Argument(ElectioneeringAggregatesGraphQLFilter, required=False))

    @cached_query
    async def resolve_electioneering_aggregates_collection(self, info, where: Union[ElectioneeringAggregatesGraphQLFilter, None] = None) -> GraphQLElectioneeringAggregatesCollection:
        result = await FecApi.get('/electioneering/aggregates', FecElectioneeringAggregatesDict, params=where.build_api_filter_dict() if where else {})

        return GraphQLElectioneeringAggregatesCollection(result.results, pagination=result.pagination)
