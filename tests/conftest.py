import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv('FEC_BASE_URL', 'http://fec.com')
    monkeypatch.setenv('FLASK_ENV', 'Development')
    monkeypatch.setenv('FLASK_DEBUG', '1')
