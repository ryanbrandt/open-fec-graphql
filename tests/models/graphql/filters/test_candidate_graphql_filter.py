import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture

from app.models.graphql.filters.candidate_graphql_filter import CandidateGraphQLFilter
from app.models.graphql.filters.base_graphql_filter import BaseGraphQLFilter


def test_build_api_filter_dict_calls_super(mocker: MockerFixture):
    MOCK_SUPER_FILTER = {'something': 'value'}

    filter = CandidateGraphQLFilter()

    spy = mocker.patch.object(
        BaseGraphQLFilter, 'build_api_filter_dict', return_value=MOCK_SUPER_FILTER)
    result = filter.build_api_filter_dict()

    assert spy.call_count == 1
    assert result == {} | MOCK_SUPER_FILTER


def test_build_api_filter_dict_with_candidate_id():
    MOCK_CANDIDATE_ID_IN = ['idOne', 'idTwo']

    filter = CandidateGraphQLFilter(candidate_id_in=MOCK_CANDIDATE_ID_IN)

    result = filter.build_api_filter_dict()

    assert result == {'candidate_id': MOCK_CANDIDATE_ID_IN}


def test_build_api_filter_dict_with_name_contains():
    MOCK_NAME_CONTIANS = 'foo'

    filter = CandidateGraphQLFilter(name_contains=MOCK_NAME_CONTIANS)

    result = filter.build_api_filter_dict()

    assert result == {'q': MOCK_NAME_CONTIANS}


def test_build_api_filter_dict_with_party_in():
    MOCK_PARTY_IN = ['REP', 'DEM']

    filter = CandidateGraphQLFilter(party_in=MOCK_PARTY_IN)

    result = filter.build_api_filter_dict()

    assert result == {'party': MOCK_PARTY_IN}


def test_build_api_filter_dict_with_office_in():
    MOCK_OFFICE_IN = ['H', 'S']

    filter = CandidateGraphQLFilter(office_in=MOCK_OFFICE_IN)

    result = filter.build_api_filter_dict()

    assert result == {'office': MOCK_OFFICE_IN}
