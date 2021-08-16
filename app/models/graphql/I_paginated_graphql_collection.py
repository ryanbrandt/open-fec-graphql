from app.models.candidate import Candidate
import graphene

from .graphql_pagination import GraphQLPagination


class IPaginatedGraphQLCollection(graphene.Interface):
    pagination = graphene.Field(lambda: GraphQLPagination)
