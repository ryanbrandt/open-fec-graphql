import graphene

from app.models.dicts.fec_pagination_dict import FecPaginationDict
from app.models.graphql.graphql_pagination import GraphQLPagination


class BaseGraphQLCollection(graphene.ObjectType):
    pagination = graphene.Field(GraphQLPagination)

    def __init__(self, pagination=FecPaginationDict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagination = GraphQLPagination(pagination)
