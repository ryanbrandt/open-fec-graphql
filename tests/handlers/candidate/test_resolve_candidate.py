import pytest
from pytest_mock import MockerFixture

from tests.mock import MOCK_EMPTY_RESPONSE
from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.models.graphql.graphql_candidate import GraphQLCandidate
from app.handlers.candidate.queries import Query
from app.models.fec_response import FecResponse

query = Query()


@pytest.mark.asyncio
async def test_resolve_candidate_calls_api(mocker: MockerFixture):
    MOCK_ID = 'id'

    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_candidate(None, MOCK_ID)

    assert spy.call_count == 1
    assert spy.call_args.args == (f'/candidate/{MOCK_ID}', FecCandidateDict)


@pytest.mark.asyncio
async def test_resolve_candidate_no_results_returns_None(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_candidate(None, 'id')

    assert result == None


@pytest.mark.asyncio
async def test_resolve_candidate_with_results_returns_Candidate(mocker: MockerFixture):
    MOCK_CANDIDATE = {'candidate_id': 'some_id'}
    MOCK_RESPONSE = FecResponse(
        [MOCK_CANDIDATE], {'page': 1, 'count': 1, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_RESPONSE)

    result = await query.resolve_candidate(None, 'id')

    assert result.__dict__ == GraphQLCandidate(MOCK_CANDIDATE).__dict__
