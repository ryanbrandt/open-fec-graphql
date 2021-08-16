import pytest
from pytest_mock import MockerFixture

from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.graphql.graphql_candidate_collection import GraphQLCandidateCollection
from app.handlers.candidate.queries import Query
from app.models.fec_response import FecResponse

query = Query()

MOCK_EMPTY_RESPONSE = FecResponse(
    [], {'page': 1, 'count': 0, 'pages': 1, 'per_page': 20})


def assert_collection_equality(actual: GraphQLCandidateCollection, expected: GraphQLCandidateCollection):
    assert actual.pagination.__dict__ == expected.pagination.__dict__

    assert all([actual_candidate.__dict__ == expected_candidate.__dict__ for actual_candidate,
               expected_candidate in zip(actual.items, expected.items)])


@pytest.mark.asyncio
async def test_resolve_candidate_collection_calls_api(mocker: MockerFixture):
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_candidate_collection(None)

    assert spy.call_count == 1
    assert spy.call_args.args == ('/candidates', FecCandidateDict)


@pytest.mark.asyncio
async def test_resolve_candidate_collection_no_results_returns_empy_list(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_candidate_collection(None)

    assert_collection_equality(result, GraphQLCandidateCollection(
        MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination))


@pytest.mark.asyncio
async def test_resolve_candidate_collection_with_results_returns_Candidate_list(mocker: MockerFixture):
    MOCK_CANDIDATE_ONE = {'candidate_id': 'some_id'}
    MOCK_CANDIDATE_TWO = {'candidate_id': 'some_other_id'}
    MOCK_RESPONSE = FecResponse(
        [MOCK_CANDIDATE_ONE, MOCK_CANDIDATE_TWO], {'page': 1, 'count': 2, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_RESPONSE)

    result = await query.resolve_candidate_collection(None)

    assert_collection_equality(result, GraphQLCandidateCollection(
        MOCK_RESPONSE.results, pagination=MOCK_RESPONSE.pagination))
