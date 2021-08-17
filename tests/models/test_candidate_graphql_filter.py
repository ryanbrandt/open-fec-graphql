from pytest_mock import MockerFixture

from app.models.graphql.candidate_graphql_filter import CandidateGraphQLFilter
from app.models.graphql.base_graphql_filter import BaseGraphQLFilter


def test_build_api_filter_dict_calls_super(mocker: MockerFixture):
    MOCK_SUPER_FILTER = {'something': 'value'}

    filter = CandidateGraphQLFilter()

    spy = mocker.patch.object(
        BaseGraphQLFilter, 'build_api_filter_dict', return_value=MOCK_SUPER_FILTER)
    result = filter.build_api_filter_dict()

    assert spy.call_count == 1
    assert result == {} | MOCK_SUPER_FILTER
