import pandas as pd
from datetime import datetime
from src.database import operations
from tests.conftest import FakeResult


def test_fetch_data_health_matrix(monkeypatch, fake_client_factory):
    rows = [
        ("2024-01-01 14:30:00", "AAPL", "REG"),
        ("2024-01-01 14:31:00", "AAPL", "REG"),
        ("2024-01-02 14:30:00", "MSFT", "REG"),
    ]
    results = {
        "FROM market_data": FakeResult(rows=rows),
    }
    fake_client = fake_client_factory(results=results)

    monkeypatch.setattr(operations, "get_db_connection", lambda: fake_client)

    start_date = datetime(2024, 1, 1).date()
    end_date = datetime(2024, 1, 2).date()

    pivot = operations.fetch_data_health_matrix(
        ["AAPL", "MSFT"], start_date, end_date, session_filter="Total"
    )

    assert not pivot.empty
    assert "AAPL" in pivot.index
    assert "MSFT" in pivot.index
