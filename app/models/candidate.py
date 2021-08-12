import graphene

from app.models.base_graphql_model import BaseGraphQLModel
from app.models.dicts.fec_candidate_dict import FecCandidateDict


class Candidate(BaseGraphQLModel[FecCandidateDict], graphene.ObjectType):
    candidate_id = graphene.String()
    name = graphene.String()

    def __init__(self, candidate: FecCandidateDict, *args, **kwargs):
        super().__init__(result_dict=candidate, *args, **kwargs)
        self.collect_attributes()
