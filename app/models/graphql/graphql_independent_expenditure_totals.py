import graphene

from app.models.dicts.fec_independent_expenditure_totals_dict import FecIndependentExpenditureTotalsDict
from .base_graphql_model import BaseGraphQLModel


class GraphQLIndependentExpenditureTotals(BaseGraphQLModel[FecIndependentExpenditureTotalsDict], graphene.ObjectType):
    cycle = graphene.Int()
    support_oppose_indicator = graphene.String()
    total = graphene.Int()
    candidate = graphene.Field(
        'app.models.graphql.graphql_candidate.GraphQLCandidate')

    def __init__(self, expenditure_totals=FecIndependentExpenditureTotalsDict, *args, **kwargs) -> None:
        super().__init__(result_dict=expenditure_totals, *args, **kwargs)
        self.collect_attributes()

    def __get_candidate_queries(self):
        from app.handlers.candidate.queries import Query as CandidateQueries

        return CandidateQueries()

    async def resolve_candidate(self, info):
        return await self.__get_candidate_queries().resolve_candidate(info, id=self.result_dict['candidate_id'])
