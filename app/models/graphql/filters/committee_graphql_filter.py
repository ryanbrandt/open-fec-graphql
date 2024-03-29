import graphene

from app.models.graphql.enums.candidate_party_enum import CandidatePartyEnum
from app.models.dicts.fec_committee_search_filter_dict import FecCommitteeSearchFilterDict
from .base_graphql_filter import BaseGraphQLFilter


class CommitteeGraphQLFilter(BaseGraphQLFilter, graphene.InputObjectType):
    committee_id_in = graphene.List(
        graphene.String, required=False, default=None)
    candidate_id_in = graphene.List(
        graphene.String, required=False, default=None)
    cycle_in = graphene.List(
        graphene.Int, required=False, default=None)
    party_in = graphene.List(CandidatePartyEnum)

    def __init__(self, candidate_id_in: list[str] = None, committee_id_in: list[str] = None, cycle_in: list[int] = None, party_in: list[CandidatePartyEnum] = None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate_id_in = candidate_id_in
        self.committee_id_in = committee_id_in
        self.cycle_in = cycle_in
        self.party_in = party_in

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecCommitteeSearchFilterDict = {}

        if self.committee_id_in:
            filter_dict['committee_id'] = [
                str(id) for id in iter(self.committee_id_in)]

        if self.candidate_id_in:
            filter_dict['candidate_id'] = [
                str(id) for id in iter(self.candidate_id_in)]

        if self.cycle_in:
            filter_dict['cycle'] = [int(c) for c in iter(self.cycle_in)]

        if self.party_in:
            filter_dict['party'] = [str(p) for p in iter(self.party_in)]

        return filter_dict | super().build_api_filter_dict()
