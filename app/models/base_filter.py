import graphene


class BaseFilter:
    id_in: graphene.List(str)
