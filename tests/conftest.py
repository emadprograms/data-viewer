import os
import types
import pytest


class DummyLogger:
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)


@pytest.fixture()
def dummy_logger():
    return DummyLogger()


@pytest.fixture()
def clear_infisical_env(monkeypatch):
    for key in ["INFISICAL_CLIENT_ID", "INFISICAL_CLIENT_SECRET", "INFISICAL_PROJECT_ID"]:
        monkeypatch.delenv(key, raising=False)
    return True


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


@pytest.fixture()
def fake_response_factory():
    def _factory(status_code=200, json_data=None, text=""):
        return FakeResponse(status_code=status_code, json_data=json_data, text=text)

    return _factory


@pytest.fixture()
def temp_env(monkeypatch):
    def _setter(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)
    return _setter


class FakeResult:
    def __init__(self, rows=None, single=None):
        self._rows = rows if rows is not None else []
        self._single = single

    def fetchone(self):
        if self._single is not None:
            return self._single
        return self._rows[0] if self._rows else None

    def fetchall(self):
        return self._rows


class FakeClient:
    def __init__(self, results=None):
        self.results = results or {}
        self.executed = []
        self.committed = False

    def execute(self, query, params=None):
        self.executed.append((query, params))
        for key, value in self.results.items():
            if key in query:
                return value
        return FakeResult()

    def commit(self):
        self.committed = True


@pytest.fixture()
def fake_client_factory():
    def _factory(results=None):
        return FakeClient(results=results)
    return _factory
