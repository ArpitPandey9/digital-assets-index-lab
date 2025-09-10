# tests/test_coingecko.py
from src.data.coingecko import get_prices_daily

def test_btc_schema_and_days():
    df = get_prices_daily("bitcoin", "usd", lookback_days=365)
    # Schema check
    assert set(["open","high","low","close","vol","missing_hours"]).issubset(df.columns)
    # At least ~360 days of data
    assert len(df) >= 360
    # Dates are increasing and UTC
    assert df.index.is_monotonic_increasing
    assert df.index.tz is not None
    # Prices are positive
    assert (df["close"] > 0).all()
