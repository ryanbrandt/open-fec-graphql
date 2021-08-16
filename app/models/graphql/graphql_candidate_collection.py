from app.models.graphql.graphql_pagination import GraphQLPagination
from app.models.dicts.fec_pagination_dict import FecPaginationDict
from app.models.graphql.graphql_candidate import GraphQLCandidate
import graphene
from typing import List

from .base_graphql_collection import BaseGraphQLCollection
from app.models.dicts.fec_candidate_dict import FecCandidateDict


class GraphQLCandidateCollection(BaseGraphQLCollection, graphene.ObjectType):
    items = graphene.List(GraphQLCandidate)

    def __init__(self, candidates: List[FecCandidateDict], pagination: FecPaginationDict, *args, **kwargs):
        super().__init__(pagination, *args, **kwargs)
        self.items = [GraphQLCandidate(c) for c in candidates]
