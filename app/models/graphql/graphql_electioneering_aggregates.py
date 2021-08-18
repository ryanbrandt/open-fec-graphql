import graphene

import app.models.graphql.graphql_candidate
import app.handlers.candidate.queries

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
        lambda: app.models.graphql.graphql_candidate.GraphQLCandidate)

    def __init__(self, aggregates=FecElectioneeringAggregatesDict, *args, **kwargs) -> None:
        super().__init__(result_dict=aggregates, *args, **kwargs)
        self.collect_attributes()

    async def resolve_candidate(self, info):
        return await app.handlers.candidate.queries.Query().resolve_candidate(info, id=self.result_dict['candidate_id'])
