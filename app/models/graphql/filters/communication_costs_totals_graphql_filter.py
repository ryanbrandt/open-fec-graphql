import graphene

from .base_graphql_filter import BaseGraphQLFilter
from app.models.dicts.fec_communication_costs_totals_search_filter_dict import FecCommunicationCostsTotalsSearchFilterDict


class CommunicationCostsTotalsGraphQLFilter(BaseGraphQLFilter, graphene.InputObjectType):
    candidate_id_in = graphene.List(
        graphene.String, required=False, default=None)
    cycle_in = graphene.List(
        graphene.Int, required=False, default=None)

    def __init__(self, candidate_id_in: list[str] = None, cycle_in: list[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate_id_in = candidate_id_in
        self.cycle_in = cycle_in

    def build_api_filter_dict(self) -> dict:
        filter_dict: FecCommunicationCostsTotalsSearchFilterDict = {}

        if self.candidate_id_in:
            filter_dict['candidate_id'] = [
                str(id) for id in iter(self.candidate_id_in)]

        if self.cycle_in:
            filter_dict['cycle'] = [int(c) for c in iter(self.cycle_in)]

        return filter_dict | super().build_api_filter_dict()
