import graphene

from .base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_candidate_dict import FecCandidateDict


class GraphQLCandidate(BaseGraphQLModel[FecCandidateDict], graphene.ObjectType):
    candidate_id = graphene.String()
    name = graphene.String()
    office_full = graphene.String()
    state = graphene.String()
    party_full = graphene.String()
    election_years = graphene.List(graphene.String)
    district = graphene.String()
    district_number = graphene.Int()

    def __init__(self, candidate: FecCandidateDict, *args, **kwargs):
        super().__init__(result_dict=candidate, *args, **kwargs)
        self.collect_attributes()
