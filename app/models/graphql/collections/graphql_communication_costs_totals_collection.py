import graphene

from .base_graphql_collection import BaseGraphQLCollection
from app.models.graphql.graphql_communication_costs_totals import GraphQLCommunicationCostsTotals
from app.models.dicts.fec_communication_costs_totals_dict import FecCommunicationCostsTotalsDict
from app.models.dicts.fec_pagination_dict import FecPaginationDict


class GraphQLCommunicationCostsTotalsCollection(BaseGraphQLCollection, graphene.ObjectType):
    items = graphene.List(GraphQLCommunicationCostsTotals)

    def __init__(self, costs_totals: list[FecCommunicationCostsTotalsDict], pagination: FecPaginationDict, *args, **kwargs):
        super().__init__(pagination=pagination, *args, **kwargs)
        self.items = [GraphQLCommunicationCostsTotals(
            ct) for ct in costs_totals]
