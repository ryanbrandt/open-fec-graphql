from app.models.graphql.base_graphql_filter import BaseGraphQLFilter


def test_build_api_filter_dict_no_page_returns_empty_dict():
    filter = BaseGraphQLFilter()

    assert filter.build_api_filter_dict() == {}


def test_build_api_filter_dict_with_page_returns_populated_dict():
    filter = BaseGraphQLFilter(page=2)

    assert filter.build_api_filter_dict() == {'page': 2}
