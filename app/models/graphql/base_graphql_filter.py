import graphene


class BaseGraphQLFilter(graphene.InputObjectType):
    id_in = graphene.List(graphene.String)
