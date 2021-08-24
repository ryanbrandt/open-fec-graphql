import graphene

from app.models.graphql.enums.candidate_office_enum import CandidateOfficeEnum
from app.models.graphql.enums.candidate_party_enum import CandidatePartyEnum
from app.models.dicts.fec_candidate_search_filter_dict import FecCandidateSearchFilterDict
from .base_graphql_filter import BaseGraphQLFilter


class CandidateGraphQLFilter(BaseGraphQLFilter, graphene.InputObjectType):
    candidate_id_in = graphene.List(
        graphene.String, required=False, default=None)
    name_contains = graphene.String(required=False, default=None)
    office_in = graphene.List(CandidateOfficeEnum)
    party_in = graphene.List(CandidatePartyEnum)

    def __init__(self, candidate_id_in: list[str] = None, name_contains: str = None, office_in: list[CandidateOfficeEnum] = None, party_in: list[CandidatePartyEnum] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate_id_in = candidate_id_in
        self.name_contains = name_contains
        self.office_in = office_in
        self.party_in = party_in

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecCandidateSearchFilterDict = {}

        if self.candidate_id_in:
            filter_dict['candidate_id'] = [
                str(id) for id in iter(self.candidate_id_in)]

        if self.name_contains:
            filter_dict['q'] = str(self.name_contains)

        if self.party_in:
            filter_dict['party'] = [str(party)
                                    for party in iter(self.party_in)]

        if self.office_in:
            filter_dict['office'] = [str(office)
                                     for office in iter(self.office_in)]

        return filter_dict | super().build_api_filter_dict()
