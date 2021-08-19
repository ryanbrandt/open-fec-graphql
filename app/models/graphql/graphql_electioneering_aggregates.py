import graphene

from .base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict


class GraphQLElectioneeringAggregates(BaseGraphQLModel, graphene.ObjectType):
    committee = graphene.String()
    committee_id = graphene.String()
    committee_name = graphene.String()
    count = graphene.Int()
    cycle = graphene.Int()
    total = graphene.Int()
    candidate = graphene.Field(
        'app.models.graphql.graphql_candidate.GraphQLCandidate')

    def __init__(self, aggregates=FecElectioneeringAggregatesDict, *args, **kwargs) -> None:
        super().__init__(result_dict=aggregates, *args, **kwargs)
        self.collect_attributes()

    def get_candidate_queries(self):
        from app.handlers.candidate.queries import Query as CandidateQueries

        return CandidateQueries()

    async def resolve_candidate(self, info):
        return await self.get_candidate_queries().resolve_candidate(info, id=self.result_dict['candidate_id'])
