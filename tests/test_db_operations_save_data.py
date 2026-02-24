import pandas as pd
from datetime import datetime, timezone
from src.database import operations


def test_save_data_to_turso_inserts(monkeypatch, fake_client_factory):
    fake_client = fake_client_factory()
    monkeypatch.setattr(operations, "get_db_connection", lambda: fake_client)
    monkeypatch.setattr(operations.time, "sleep", lambda *_: None)

    df = pd.DataFrame(
        [
            {
                "timestamp": datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
                "symbol": "AAPL",
                "open": 1.0,
                "high": 2.0,
                "low": 0.5,
                "close": 1.5,
                "volume": 10.0,
                "session": "REG",
            }
        ]
    )

    ok = operations.save_data_to_turso(df)

    assert ok is True
    assert fake_client.committed is True
    assert any("INSERT OR REPLACE INTO market_data" in q for q, _ in fake_client.executed)


def test_save_data_to_turso_empty(monkeypatch, fake_client_factory):
    fake_client = fake_client_factory()
    monkeypatch.setattr(operations, "get_db_connection", lambda: fake_client)

    df = pd.DataFrame()
    ok = operations.save_data_to_turso(df)

    assert ok is False
