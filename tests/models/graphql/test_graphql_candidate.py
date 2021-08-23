import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from app.models.graphql.filters.base_graphql_filter import BaseGraphQLFilter
from app.models.graphql.filters.electioneering_aggregates_graphql_filter import ElectioneeringAggregatesGraphQLFilter
from app.models.graphql.graphql_electioneering_aggregates_collection import GraphQLElectioneeringAggregatesCollection
from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.graphql.graphql_candidate import GraphQLCandidate
from tests.mock import MOCK_EMPTY_RESPONSE


MOCK_CANDIDATE_DICT: FecCandidateDict = {
    'candidate_id': 'SomeID'
}

MOCK_AGGREGATES_COLLECTION = GraphQLElectioneeringAggregatesCollection(
    MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination)


@pytest.fixture()
def mocked_aggregates_resolver(mocker: MockerFixture):
    spy = mocker.patch('app.handlers.electioneering.queries.Query.resolve_electioneering_aggregates_collection',
                       return_value=MOCK_AGGREGATES_COLLECTION)

    return spy


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_without_where(mocked_aggregates_resolver: MagicMock):
    candidate = GraphQLCandidate(candidate=MOCK_CANDIDATE_DICT)

    result = await candidate.resolve_electioneering_aggregates_collection(None)

    mocked_aggregates_resolver.assert_called_once_with(
        None, where=ElectioneeringAggregatesGraphQLFilter(candidate_id_in=[candidate.candidate_id], **{}))

    assert result.__dict__ == MOCK_AGGREGATES_COLLECTION.__dict__


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_with_where(mocked_aggregates_resolver: MagicMock):
    MOCK_FILTER = BaseGraphQLFilter(per_page=50)

    candidate = GraphQLCandidate(candidate=MOCK_CANDIDATE_DICT)

    result = await candidate.resolve_electioneering_aggregates_collection(None, where=MOCK_FILTER)

    mocked_aggregates_resolver.assert_called_once_with(
        None, where=ElectioneeringAggregatesGraphQLFilter(candidate_id_in=[candidate.candidate_id], **MOCK_FILTER.build_api_filter_dict()))

    assert result.__dict__ == MOCK_AGGREGATES_COLLECTION.__dict__
