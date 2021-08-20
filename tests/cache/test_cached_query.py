import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock

from app.models.graphql.graphql_candidate import GraphQLCandidate
from app.cache.cached_query import cached_query


MOCK_CACHED_CANDIDATE = GraphQLCandidate({'candidate_id': 'SomeId'})

MOCK_COMPUTED_CANDIDATE = GraphQLCandidate({'candidate_id': 'SomeOtherId'})


@pytest.fixture()
def mocked_fn():
    mock_fn = AsyncMock(return_value=MOCK_COMPUTED_CANDIDATE)
    mock_fn.__name__ = 'name'

    return mock_fn


@pytest.mark.asyncio
async def test_cached_query_cache_miss(mocker: MockerFixture, mocked_fn: AsyncMock):
    mock_args = ['some_arg']
    mock_kwargs = {
        'some': 'kwarg'
    }

    mocker.patch('redis.Redis.get', return_value=None)

    wrapped_fn = cached_query(mocked_fn)
    result = await wrapped_fn(*mock_args, **mock_kwargs)

    mocked_fn.assert_called_once_with(*mock_args, **mock_kwargs)

    assert result.__dict__ == MOCK_COMPUTED_CANDIDATE.__dict__
