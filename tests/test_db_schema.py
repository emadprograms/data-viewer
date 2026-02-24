from src.database import schema
from tests.conftest import FakeResult


def test_init_db_creates_tables(monkeypatch, fake_client_factory):
    results = {
        "SELECT count(*) FROM market_symbols": FakeResult(single=(0,)),
    }
    fake_client = fake_client_factory(results=results)

    monkeypatch.setattr(schema, "get_db_connection", lambda: fake_client)
    monkeypatch.setattr(schema.st, "runtime", type("R", (), {"exists": lambda: False})())

    schema.init_db()

    executed = "\n".join(q for q, _ in fake_client.executed)
    assert "CREATE TABLE IF NOT EXISTS market_symbols" in executed
    assert "CREATE TABLE IF NOT EXISTS market_data" in executed
