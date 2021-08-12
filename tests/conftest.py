import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'Production')
    monkeypatch.setenv('FLASK_DEBUG', '0')
