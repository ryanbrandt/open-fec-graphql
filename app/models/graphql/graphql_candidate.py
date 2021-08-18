from typing import Union
import graphene

import app.handlers.electioneering.queries
import app.models.graphql.graphql_electioneering_aggregates_collection

from app.models.graphql.filters.electioneering_aggregates_filter import ElectioneeringAggregatesFilter
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
        lambda: app.models.graphql.graphql_electioneering_aggregates_collection.GraphQLElectioneeringAggregatesCollection, where=graphene.Argument(BaseGraphQLFilter, required=False))

    def __init__(self, candidate: FecCandidateDict, *args, **kwargs):
        super().__init__(result_dict=candidate, *args, **kwargs)
        self.collect_attributes()

    async def resolve_electioneering_aggregates_collection(self, info, where: Union[BaseGraphQLFilter, None] = None):
        filter_dict = where.build_api_filter_dict() if where else {}

        return await app.handlers.electioneering.queries.Query().resolve_electioneering_aggregates_collection(info, where=ElectioneeringAggregatesFilter(candidate_id_in=[self.candidate_id], **filter_dict))
