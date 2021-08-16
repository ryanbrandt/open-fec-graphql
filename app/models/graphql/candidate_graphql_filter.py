import graphene

from .base_graphql_filter import BaseGraphQLFilter


class CandidateGraphQLFilter(BaseGraphQLFilter, graphene.InputObjectType):
    name_contains = graphene.String()
    office_equals: graphene.String()
    party_equals: graphene.String()
