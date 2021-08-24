from typing import Union
import graphene

from app.models.graphql.filters.electioneering_aggregates_graphql_filter import ElectioneeringAggregatesGraphQLFilter
from app.models.graphql.filters.independent_expenditures_totals_graphql_filter import IndependentExpendituresTotalsGraphQLFilter
from .base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.graphql.filters.base_graphql_filter import BaseGraphQLFilter


class GraphQLCandidate(BaseGraphQLModel[FecCandidateDict], graphene.ObjectType):
    candidate_id = graphene.String()
    name = graphene.String()
    office_full = graphene.String()
    state = graphene.String()
    party_full = graphene.String()
    election_years = graphene.List(graphene.String)
    district = graphene.String()
    district_number = graphene.Int()
    electioneering_aggregates_collection = graphene.Field(
        'app.models.graphql.collections.graphql_electioneering_aggregates_collection.GraphQLElectioneeringAggregatesCollection', where=graphene.Argument(BaseGraphQLFilter, required=False))
    independent_expenditures_totals_collection = graphene.Field(
        'app.models.graphql.collections.graphql_independent_expenditure_totals_collection.GraphQLIndependentExpenditureTotalsCollection', where=graphene.Argument(BaseGraphQLFilter, required=False))

    def __init__(self, candidate: FecCandidateDict, *args, **kwargs):
        super().__init__(result_dict=candidate, *args, **kwargs)
        self.collect_attributes()

    def __get_electioneering_queries(self):
        from app.handlers.electioneering.queries import Query as ElectioneeringQueries

        return ElectioneeringQueries()

    def __get_independent_expenditures_queries(self):
        from app.handlers.independent_expenditures.queries import Query as IndependentExpendituresQueries

        return IndependentExpendituresQueries()

    async def resolve_electioneering_aggregates_collection(self, info, where: Union[BaseGraphQLFilter, None] = None):
        filter_dict = where.build_api_filter_dict() if where else {}

        return await self.__get_electioneering_queries().resolve_electioneering_aggregates_collection(info, where=ElectioneeringAggregatesGraphQLFilter(candidate_id_in=[self.candidate_id], **filter_dict))

    async def resolve_independent_expenditures_totals_collection(self, info,  where: Union[BaseGraphQLFilter, None] = None):
        filter_dict = where.build_api_filter_dict() if where else {}

        return await self.__get_independent_expenditures_queries().resolve_independent_expenditure_totals(info, where=IndependentExpendituresTotalsGraphQLFilter(candidate_id_in=[self.candidate_id], **filter_dict))
