import graphene

from app.models.dicts.fec_independent_expenditure_totals_dict import FecIndependentExpenditureTotalsDict
from app.models.graphql.collections.graphql_independent_expenditure_totals_collection import GraphQLIndependentExpenditureTotalsCollection
from app.utils.api import FecApi
from app.utils.setup_logger import get_logger
from app.cache.cached_query import cached_query


class Query(graphene.ObjectType):
    LOGGER = get_logger(__name__)

    independent_expenditure_totals = graphene.Field(
        GraphQLIndependentExpenditureTotalsCollection)

    @cached_query
    async def resolve_independent_expenditure_totals(self, info):
        result = await FecApi.get('/schedules/schedule_e/totals/by_candidate/', FecIndependentExpenditureTotalsDict)

        return GraphQLIndependentExpenditureTotalsCollection(result.results, pagination=result.pagination)
