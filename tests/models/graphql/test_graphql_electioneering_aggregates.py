import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict
from app.models.graphql.graphql_candidate import GraphQLCandidate
from app.models.graphql.graphql_electioneering_aggregates import GraphQLElectioneeringAggregates

MOCK_AGGREGATES_DICT: FecElectioneeringAggregatesDict = {
    'candidate_id': 'SomeID',
    'cycle': 2020
}

MOCK_CANDIDATE = GraphQLCandidate(
    {'candidate_id': 'SomeID'})


@pytest.fixture()
def mocked_candidate_resolver(mocker: MockerFixture):
    spy = mocker.patch(
        'app.handlers.candidate.queries.Query.resolve_candidate', return_value=MOCK_CANDIDATE)

    return spy


@pytest.mark.asyncio
async def test_resolve_candidate(mocked_candidate_resolver: MagicMock):
    aggregates = GraphQLElectioneeringAggregates(
        aggregates=MOCK_AGGREGATES_DICT)

    result = await aggregates.resolve_candidate(None)

    mocked_candidate_resolver.assert_called_once_with(
        None, id=MOCK_AGGREGATES_DICT['candidate_id'])

    assert result.__dict__ == MOCK_CANDIDATE.__dict__
