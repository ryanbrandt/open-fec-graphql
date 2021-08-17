import graphene

from app.models.dicts.fec_candidate_search_filter_dict import FecCandidateSearchFilterDict
from .base_graphql_filter import BaseGraphQLFilter


class CandidatePartyEnum(graphene.Enum):
    DEMOCRAT = 'DEM'
    REPUBLICAN = 'REP'
    LIBERTARIAN = 'LIB'
    GREEN = 'GRE'
    SOCIALIST = 'SOC'


class CandidateOfficeEnum(graphene.Enum):
    HOUSE = 'H'
    SENATE = 'S'
    PRESIDENT = 'P'


class CandidateGraphQLFilter(BaseGraphQLFilter, graphene.InputObjectType):
    name_contains = graphene.String(required=False, default=None)
    office_in = graphene.List(CandidateOfficeEnum)
    party_in = graphene.List(CandidatePartyEnum)

    def __init__(self, name_contains=None, office_in=None, party_in=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_contains = name_contains
        self.office_in = office_in
        self.party_in = party_in

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecCandidateSearchFilterDict = {}

        if self.id_in:
            filter_dict['candidate_id'] = [str(id) for id in iter(self.id_in)]

        if self.name_contains:
            filter_dict['q'] = str(self.name_contains)

        if self.party_in:
            filter_dict['party'] = [str(party)
                                    for party in iter(self.party_in)]

        if self.office_in:
            filter_dict['office'] = [str(office)
                                     for office in iter(self.office_in)]

        return filter_dict | super().build_api_filter_dict()
