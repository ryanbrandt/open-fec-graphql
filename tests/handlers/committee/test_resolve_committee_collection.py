from app.models.fec_response import FecResponse
import pytest
from pytest_mock import MockerFixture

from app.models.graphql.collections.graphql_committee_collection import GraphQLCommitteeCollection
from app.models.graphql.filters.committee_graphql_filter import CommitteeGraphQLFilter
from tests.mock import MOCK_EMPTY_RESPONSE
from app.models.dicts.fec_committee_dict import FecCommitteeDict
from app.handlers.committee.queries import Query

query = Query()


def assert_collection_equality(actual: GraphQLCommitteeCollection, expected: GraphQLCommitteeCollection):
    assert actual.pagination.__dict__ == expected.pagination.__dict__

    assert all([actual_candidate.__dict__ == expected_candidate.__dict__ for actual_candidate,
               expected_candidate in zip(actual.items, expected.items)])


@pytest.mark.asyncio
async def test_resolve_committee_collection_calls_api(mocker: MockerFixture):
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_committee_collection(None)

    spy.assert_called_once_with('/committees', FecCommitteeDict, params={})


@pytest.mark.asyncio
async def test_resolve_committee_collection_applies_filter_params(mocker: MockerFixture):
    MOCK_FILTER = CommitteeGraphQLFilter(candidate_id_in=['someId'])
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_committee_collection(None, where=MOCK_FILTER)

    spy.assert_called_once_with(
        '/committees', FecCommitteeDict, params=MOCK_FILTER.build_api_filter_dict())


@pytest.mark.asyncio
async def test_resolve_committee_collection_no_results_returns_empty_list(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_committee_collection(None, None)

    assert_collection_equality(
        result, GraphQLCommitteeCollection(committees=MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination))


@pytest.mark.asyncio
async def test_resolve_committee_collection_with_results_returns_populated_list(mocker: MockerFixture):
    MOCK_RESPONSE = FecResponse(
        [{'committee_id': 'someId'}], {'page': 1, 'count': 1, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_RESPONSE)

    result = await query.resolve_committee_collection(None, None)

    assert_collection_equality(
        result, GraphQLCommitteeCollection(
            committees=MOCK_RESPONSE.results, pagination=MOCK_RESPONSE.pagination))
