import pytest
from pytest_mock import MockerFixture

from app.models.graphql.graphql_committee import GraphQLCommittee
from app.models.fec_response import FecResponse
from tests.mock import MOCK_EMPTY_RESPONSE
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.handlers.committee.queries import Query

query = Query()


@pytest.mark.asyncio
async def test_resolve_candidate_calls_api(mocker: MockerFixture):
    MOCK_ID = 'SomeID'

    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_committee(None, MOCK_ID)

    spy.assert_called_once_with(f'/committee/{MOCK_ID}', FecCommitteeDict)


@pytest.mark.asyncio
async def test_resolve_committee_no_results_returns_None(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_committee(None, '')

    assert result == None


@pytest.mark.asyncio
async def test_resolve_committee_results_returns_GraphQLCommittee(mocker: MockerFixture):
    MOCK_COMMITTEE: FecCommitteeDict = {
        'committee_id': 'SomeId'
    }
    MOCK_RESPONSE = FecResponse(
        [MOCK_COMMITTEE], {'page': 1, 'count': 1, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_RESPONSE)

    result = await query.resolve_committee(None, '')

    assert result.__dict__ == GraphQLCommittee(MOCK_COMMITTEE).__dict__
