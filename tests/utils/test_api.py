import pytest
from aioresponses import aioresponses
from typing import Any
from graphql.error import GraphQLError

from app.models.dicts.fec_candidate_dict import FecCandidateDict
from app.utils.api import FecApi
from app.app import create_app

MOCK_AUTHORIZED_URL = '/graphql?api_key=key'
BASE_URL = 'http://fec.com'


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as response:
        yield response


@pytest.mark.asyncio
async def test_fec_api_get_no_api_key_raises():
    with create_app().test_request_context('/graphql'):

        with pytest.raises(GraphQLError):
            await FecApi.get('/foo', Any)


@pytest.mark.asyncio
async def test_fec_api_get_not_ok_raises(mock_aioresponse: aioresponses):
    with create_app().test_request_context('/graphql?api_key=key'):
        mock_aioresponse.get(f'{BASE_URL}/foo?api_key=key', status=400)

        with pytest.raises(GraphQLError):
            await FecApi.get('/foo', Any)


@pytest.mark.asyncio
async def test_fec_api_get_ok_returns_FecResponse_of_T(mock_aioresponse: aioresponses):
    MOCK_RESPONSE = {
        'results': [
            {
                'candidate_id': 'id'
            }
        ],
        'pagination': {'page': 1, 'count': 1, 'pages': 1, 'per_page': 20}
    }

    with create_app().test_request_context('/graphql?api_key=key'):
        mock_aioresponse.get(f'{BASE_URL}/foo?api_key=key',
                             status=200, payload=MOCK_RESPONSE)

        result = await FecApi.get('/foo', FecCandidateDict)

        assert result.pagination == MOCK_RESPONSE['pagination']
        assert all([isinstance(actual, dict)
                   for actual in result.results])
        assert all([actual == expected for actual, expected in zip(
            result.results, MOCK_RESPONSE['results'])])
