import pytest
from pytest_mock import MockerFixture

from app.models.graphql.graphql_candidate import GraphQLCandidate
from app.models.graphql.graphql_independent_expenditure_totals import GraphQLIndependentExpenditureTotals
from app.models.dicts.fec_independent_expenditure_totals_dict import FecIndependentExpenditureTotalsDict

MOCK_EXPENDITURES: FecIndependentExpenditureTotalsDict = {
    'total': 0,
    'candidate_id': 'someId'
}


@pytest.mark.asyncio
async def test_resolve_candidate(mocker: MockerFixture):
    MOCK_RESULT = GraphQLCandidate(candidate={'candidate_id': 'someId'})
    spy = mocker.patch(
        'app.handlers.candidate.queries.Query.resolve_candidate', return_value=MOCK_RESULT)

    expenditures = GraphQLIndependentExpenditureTotals(
        expenditure_totals=MOCK_EXPENDITURES)

    result = await expenditures.resolve_candidate(None)

    spy.assert_called_once()
    assert result == MOCK_RESULT
