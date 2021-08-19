import pytest
from pytest_mock import MockerFixture

from tests.mock import MOCK_EMPTY_RESPONSE
from app.handlers.electioneering.queries import Query
from app.models.dicts.fec_electioneering_aggregates_dict import FecElectioneeringAggregatesDict
from app.models.graphql.filters.electioneering_aggregates_filter import ElectioneeringAggregatesFilter
from app.models.graphql.graphql_electioneering_aggregates_collection import GraphQLElectioneeringAggregatesCollection
from app.models.fec_response import FecResponse

query = Query()


def assert_collection_equality(actual: GraphQLElectioneeringAggregatesCollection, expected: GraphQLElectioneeringAggregatesCollection):
    assert actual.pagination.__dict__ == expected.pagination.__dict__

    assert all([actual_candidate.__dict__ == expected_candidate.__dict__ for actual_candidate,
               expected_candidate in zip(actual.items, expected.items)])


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_calls_api(mocker: MockerFixture):
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_electioneering_aggregates_collection(None)

    assert spy.call_count == 1
    spy.assert_called_with(
        '/electioneering/aggregates', FecElectioneeringAggregatesDict, params={})


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_with_ElectioneeringAggregatesFilter_params(mocker: MockerFixture):
    MOCK_AGGREGATES_FILTER = ElectioneeringAggregatesFilter(cycle_in=[2020])

    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_electioneering_aggregates_collection(None, where=MOCK_AGGREGATES_FILTER)

    assert spy.call_count == 1
    spy.assert_called_with(
        '/electioneering/aggregates', FecElectioneeringAggregatesDict, params=MOCK_AGGREGATES_FILTER.build_api_filter_dict())


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_with_results_returns_empty_list(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_electioneering_aggregates_collection(None)

    assert_collection_equality(result, GraphQLElectioneeringAggregatesCollection(
        MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination))


@pytest.mark.asyncio
async def test_resolve_electioneering_aggregates_collection_with_results_returns_populated_list(mocker: MockerFixture):
    MOCK_AGGREGATES_ONE = {'cycle': 2020}
    MOCK_AGGREGATES_TWO = {'cycle': 2016}
    MOCK_RESPONSE = FecResponse(
        [MOCK_AGGREGATES_ONE, MOCK_AGGREGATES_TWO], {'page': 1, 'count': 2, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get', return_value=MOCK_RESPONSE)

    result = await query.resolve_electioneering_aggregates_collection(None)

    assert_collection_equality(result, GraphQLElectioneeringAggregatesCollection(
        MOCK_RESPONSE.results, pagination=MOCK_RESPONSE.pagination))
