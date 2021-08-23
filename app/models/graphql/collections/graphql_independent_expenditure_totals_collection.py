import graphene

from .base_graphql_collection import BaseGraphQLCollection
from app.models.graphql.graphql_independent_expenditure_totals import GraphQLIndependentExpenditureTotals
from app.models.dicts.fec_independent_expenditure_totals_dict import FecIndependentExpenditureTotalsDict
from app.models.dicts.fec_pagination_dict import FecPaginationDict


class GraphQLIndependentExpenditureTotalsCollection(BaseGraphQLCollection, graphene.ObjectType):
    items = graphene.List(GraphQLIndependentExpenditureTotals)

    def __init__(self, expenditures: list[FecIndependentExpenditureTotalsDict], pagination: FecPaginationDict, *args, **kwargs):
        super().__init__(pagination=pagination, *args, **kwargs)
        self.items = [GraphQLIndependentExpenditureTotals(
            e) for e in expenditures]
