import pytest
from pytest_mock import MockerFixture

from app.models.fec_response import FecResponse
from app.models.graphql.collections.graphql_independent_expenditure_totals_collection import GraphQLIndependentExpenditureTotalsCollection
from app.models.graphql.filters.independent_expenditures_totals_graphql_filter import IndependentExpendituresTotalsGraphQLFilter
from app.models.dicts.fec_independent_expenditure_totals_dict import FecIndependentExpenditureTotalsDict
from tests.mock import MOCK_EMPTY_RESPONSE
from app.handlers.independent_expenditures.queries import Query

query = Query()


def assert_collection_equality(actual: GraphQLIndependentExpenditureTotalsCollection, expected: GraphQLIndependentExpenditureTotalsCollection):
    assert actual.pagination.__dict__ == expected.pagination.__dict__

    assert all([actual_candidate.__dict__ == expected_candidate.__dict__ for actual_candidate,
               expected_candidate in zip(actual.items, expected.items)])


@pytest.mark.asyncio
async def test_resolve_independent_expenditure_totals_calls_api(mocker: MockerFixture):
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    await query.resolve_independent_expenditure_totals(None, None)

    spy.assert_called_once_with(
        '/schedules/schedule_e/totals/by_candidate/', FecIndependentExpenditureTotalsDict, params={})


@pytest.mark.asyncio
async def test_resolve_independent_expenditure_totals_applies_params(mocker: MockerFixture):
    spy = mocker.patch('app.utils.api.FecApi.get',
                       return_value=MOCK_EMPTY_RESPONSE)

    MOCK_FILTER = IndependentExpendituresTotalsGraphQLFilter(
        candidate_id_in=['some_id'])
    await query.resolve_independent_expenditure_totals(None, where=MOCK_FILTER)

    spy.assert_called_once_with(
        '/schedules/schedule_e/totals/by_candidate/', FecIndependentExpenditureTotalsDict, params=MOCK_FILTER.build_api_filter_dict())


@pytest.mark.asyncio
async def test_resolve_indepdent_expenditure_totals_no_results_returns_empty_list(mocker: MockerFixture):
    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_EMPTY_RESPONSE)

    result = await query.resolve_independent_expenditure_totals(None, None)

    assert_collection_equality(result, GraphQLIndependentExpenditureTotalsCollection(
        expenditures=MOCK_EMPTY_RESPONSE.results, pagination=MOCK_EMPTY_RESPONSE.pagination))


@pytest.mark.asyncio
async def test_resolve_independent_expenditure_totals_with_results_returns_populated_list(mocker: MockerFixture):
    MOCK_RESPONSE = FecResponse(
        [{'total': 0}], {'page': 1, 'count': 1, 'pages': 1, 'per_page': 20})

    mocker.patch('app.utils.api.FecApi.get',
                 return_value=MOCK_RESPONSE)

    result = await query.resolve_independent_expenditure_totals(None, None)

    assert_collection_equality(result,  GraphQLIndependentExpenditureTotalsCollection(
        expenditures=MOCK_RESPONSE.results, pagination=MOCK_RESPONSE.pagination))
