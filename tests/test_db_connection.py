import types
from src.database import connection
import src.infisical_manager as infisical_manager


def test_get_db_connection_missing_secrets(monkeypatch):
    class DummyManager:
        def get_secret(self, name):
            return None

    monkeypatch.setattr(infisical_manager, "InfisicalManager", DummyManager)
    monkeypatch.setattr(connection.st, "runtime", types.SimpleNamespace(exists=lambda: False))

    client = connection.get_db_connection()
    assert client is None


def test_get_db_connection_happy_path(monkeypatch):
    class DummyManager:
        def get_secret(self, name):
            return "value"

    fake_client = object()

    monkeypatch.setattr(infisical_manager, "InfisicalManager", DummyManager)
    monkeypatch.setattr(connection, "libsql", types.SimpleNamespace(connect=lambda url, auth_token: fake_client))
    monkeypatch.setattr(connection.st, "runtime", types.SimpleNamespace(exists=lambda: False))

    client = connection.get_db_connection()
    assert client is fake_client
