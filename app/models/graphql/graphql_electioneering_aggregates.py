import graphene

from .base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict


class GraphQLElectioneeringAggregates(BaseGraphQLModel, graphene.ObjectType):
    count = graphene.Int()
    cycle = graphene.Int()
    total = graphene.Int()
    candidate = graphene.Field(
        'app.models.graphql.graphql_candidate.GraphQLCandidate')
    commitee = graphene.Field(
        'app.models.graphql.graphql_committee.GraphQLCommittee')

    def __init__(self, aggregates=FecElectioneeringAggregatesDict, *args, **kwargs) -> None:
        super().__init__(result_dict=aggregates, *args, **kwargs)
        self.collect_attributes()

    def __get_candidate_queries(self):
        from app.handlers.candidate.queries import Query as CandidateQueries

        return CandidateQueries()

    def __get_committee_queries(self):
        from app.handlers.committee.queries import Query as CommitteeQueries

        return CommitteeQueries()

    async def resolve_candidate(self, info):
        return await self.__get_candidate_queries().resolve_candidate(info, id=self.result_dict['candidate_id'])

    async def resolve_committee(self, info):
        return await self.__get_committee_queries().resolve_committee(info, id=self.result_dict['committee_id'])
