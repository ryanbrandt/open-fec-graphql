import pytest
from unittest.mock import patch

patch('app.cache.cached_query.cached_query', lambda x: x).start()


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv('FEC_BASE_URL', 'http://fec.com')
    monkeypatch.setenv('FLASK_ENV', 'Development')
    monkeypatch.setenv('FLASK_DEBUG', '1')
