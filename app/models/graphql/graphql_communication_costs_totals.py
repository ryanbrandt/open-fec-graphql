import graphene

from app.models.dicts.fec_communication_costs_totals_dict import FecCommunicationCostsTotalsDict
from .base_graphql_model import BaseGraphQLModel


class GraphQLCommunicationCostsTotals(BaseGraphQLModel[FecCommunicationCostsTotalsDict], graphene.ObjectType):
    cycle = graphene.Int()
    total = graphene.Int()
    support_oppose_indicator = graphene.String()
    candidate = graphene.Field(
        'app.models.graphql.graphql_candidate.GraphQLCandidate')

    def __init__(self, costs_totals: FecCommunicationCostsTotalsDict, *args, **kwargs) -> None:
        super().__init__(result_dict=costs_totals, *args, **kwargs)
        self.collect_attributes()

    def __get_candidate_queries(self):
        from app.handlers.candidate.queries import Query as CandidateQueries

        return CandidateQueries()

    async def resolve_candidate(self, info):
        return await self.__get_candidate_queries().resolve_candidate(info, id=self.result_dict['candidate_id'])
