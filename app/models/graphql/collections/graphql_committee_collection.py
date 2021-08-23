import graphene
from typing import List

from .base_graphql_collection import BaseGraphQLCollection
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.models.dicts.fec_pagination_dict import FecPaginationDict
from app.models.graphql.graphql_committee import GraphQLCommittee


class GraphQLCommitteeCollection(BaseGraphQLCollection, graphene.ObjectType):
    items = graphene.List(GraphQLCommittee)

    def __init__(self, committees: List[FecCommitteeDict], pagination: FecPaginationDict, *args, **kwargs):
        super().__init__(pagination=pagination, *args, **kwargs)
        self.items = [GraphQLCommittee(c) for c in committees]
