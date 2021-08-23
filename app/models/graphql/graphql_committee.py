import graphene

from app.models.graphql.filters.candidate_graphql_filter import CandidateGraphQLFilter
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.models.graphql.graphql_candidate_collection import GraphQLCandidateCollection
from .base_graphql_model import BaseGraphQLModel


class GraphQLCommittee(BaseGraphQLModel[FecCommitteeDict], graphene.ObjectType):
    committee_id = graphene.String()
    name = graphene.String()
    party = graphene.String()
    cycles = graphene.List(graphene.Int)
    state = graphene.String()
    candidate_collection = graphene.Field(GraphQLCandidateCollection)

    def __init__(self, comittee: FecCommitteeDict, *args, **kwargs) -> None:
        super().__init__(result_dict=comittee, *args, **kwargs)
        self.collect_attributes()

    def __get_candidate_queries(self):
        from app.handlers.candidate.queries import Query as CandidateQueries

        return CandidateQueries()

    async def resolve_candidate_collection(self, info):
        return await self.__get_candidate_queries().resolve_candidate_collection(info, where=CandidateGraphQLFilter(candidate_id_in=[self.result_dict['candidate_ids']]))
