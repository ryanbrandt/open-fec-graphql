import pytest
from pytest_mock import MockerFixture

from app.models.graphql.collections.graphql_candidate_collection import GraphQLCandidateCollection
from tests.mock import MOCK_EMPTY_RESPONSE
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.models.graphql.graphql_committee import GraphQLCommittee

MOCK_COMMITTEE_DICT: FecCommitteeDict = {
    'committee_id': 'SomeId',
    'candidate_ids': []
}


@pytest.mark.asyncio
async def test_resolve_candidate_collection(mocker: MockerFixture):
    MOCK_RESULT = GraphQLCandidateCollection(
        candidates=MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination)

    committee = GraphQLCommittee(MOCK_COMMITTEE_DICT)

    spy = mocker.patch(
        'app.handlers.candidate.queries.Query.resolve_candidate_collection', return_value=MOCK_RESULT)

    result = await committee.resolve_candidate_collection(None)

    spy.assert_called_once()
    assert result == MOCK_RESULT
