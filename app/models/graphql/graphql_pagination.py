import graphene

from .base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_pagination_dict import FecPaginationDict


class GraphQLPagination(BaseGraphQLModel[FecPaginationDict], graphene.ObjectType):
    page = graphene.Int()
    count = graphene.Int()
    pages = graphene.Int()
    per_page = graphene.Int()

    def __init__(self, pagination: FecPaginationDict = {}, *args, **kwargs):
        super().__init__(result_dict=pagination, *args, **kwargs)
        self.collect_attributes()
