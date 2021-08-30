import graphene
from typing import Union

from app.utils.setup_logger import get_logger
from app.utils.api import FecApi
from app.cache.cached_query import cached_query
from app.models.dicts.fec_communication_costs_totals_dict import FecCommunicationCostsTotalsDict
from app.models.graphql.filters.communication_costs_totals_graphql_filter import CommunicationCostsTotalsGraphQLFilter
from app.models.graphql.collections.graphql_communication_costs_totals_collection import GraphQLCommunicationCostsTotalsCollection


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    communication_costs_totals = graphene.Field(
        GraphQLCommunicationCostsTotalsCollection, where=graphene.Argument(CommunicationCostsTotalsGraphQLFilter, required=False))

    @cached_query
    async def resolve_communication_costs_totals(self, info, where: Union[CommunicationCostsTotalsGraphQLFilter, None] = None):
        result = await FecApi.get('/communication_costs/totals/by_candidate', FecCommunicationCostsTotalsDict, params=where.build_api_filter_dict() if where else {})

        return GraphQLCommunicationCostsTotalsCollection(costs_totals=result.results, pagination=result.pagination)
