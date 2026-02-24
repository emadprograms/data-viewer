from src import config


def test_schema_cols_shape():
    assert isinstance(config.SCHEMA_COLS, list)
    assert config.SCHEMA_COLS[0] == "timestamp"
    assert "symbol" in config.SCHEMA_COLS


def test_timezones_present():
    assert str(config.UTC) == "UTC"
    assert "US/Eastern" in str(config.US_EASTERN)
