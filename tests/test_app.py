from app.app import create_app

MOCK_QUERY = '{candidateCollection{items{candidateId}}}'


def test_app_get_graphiql():
    with create_app().test_client() as client:
        response = client.get(
            f'/graphql?api_key=some_key&query={MOCK_QUERY}')

        assert response.status_code == 200
