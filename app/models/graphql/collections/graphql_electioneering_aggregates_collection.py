import graphene
from typing import List

from .base_graphql_collection import BaseGraphQLCollection
from app.models.graphql.graphql_electioneering_aggregates import GraphQLElectioneeringAggregates
from app.models.dicts.fec_pagination_dict import FecPaginationDict
from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict


class GraphQLElectioneeringAggregatesCollection(BaseGraphQLCollection, graphene.ObjectType):
    items = graphene.List(GraphQLElectioneeringAggregates)

    def __init__(self, aggregates: List[FecElectioneeringAggregatesDict], pagination: FecPaginationDict, *args, **kwargs):
        super().__init__(pagination=pagination, *args, **kwargs)
        self.items = [GraphQLElectioneeringAggregates(a) for a in aggregates]
