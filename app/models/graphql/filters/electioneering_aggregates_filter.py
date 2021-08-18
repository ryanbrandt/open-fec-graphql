import graphene

from app.models.dicts.fec_electioneering_aggregates_search_filter_dict import FecElectioneeringAggregatesSearchFilterDict
from .base_graphql_filter import BaseGraphQLFilter


class ElectioneeringAggregatesFilter(BaseGraphQLFilter, graphene.InputObjectType):
    candidate_id_in = graphene.List(
        graphene.String, required=False, default=None)
    committee_id_in = graphene.List(
        graphene.String, required=False, default=None)
    cycle_in = graphene.List(
        graphene.Int, required=False, default=None)

    def __init__(self, candidate_id_in=None, committee_id_in=None, cycle_in=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate_id_in = candidate_id_in
        self.committee_id_in = committee_id_in
        self.cycle_in = cycle_in

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecElectioneeringAggregatesSearchFilterDict = {}

        if self.candidate_id_in:
            filter_dict['candidate_id'] = [
                str(id) for id in iter(self.candidate_id_in)]

        if self.committee_id_in:
            filter_dict['committee_id'] = [
                str(id) for id in iter(self.committee_id_in)]

        if self.cycle_in:
            filter_dict['cycle'] = [str(id) for id in iter(self.cycle_in)]

        return filter_dict | super().build_api_filter_dict()
