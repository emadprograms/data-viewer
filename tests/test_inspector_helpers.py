import pandas as pd
from datetime import datetime, timezone
from src.ui.inspector import check_integrity


def test_check_integrity_detects_gaps_and_bad_ohlc():
    df = pd.DataFrame(
        [
            {
                "timestamp": datetime(2024, 1, 1, 14, 30, tzinfo=timezone.utc),
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
                "volume": 10,
                "session": "REG",
            },
            {
                "timestamp": datetime(2024, 1, 1, 14, 50, tzinfo=timezone.utc),
                "open": 2,
                "high": 1,  # bad
                "low": 0.5,
                "close": 1.2,
                "volume": 0,
                "session": "REG",
            },
        ]
    )

    report = check_integrity(df)

    assert report["score"] < 100
    assert not report["gaps"].empty
    assert not report["bad_ohlc"].empty
