from src.data.coingecko import get_prices_daily

def test_eth_schema_and_days():
    df = get_prices_daily("ethereum", "usd", lookback_days=365)
    assert set(["open","high","low","close","vol","missing_hours"]).issubset(df.columns)
    assert len(df) >= 360
    assert df.index.is_monotonic_increasing
    assert df.index.tz is not None
    assert (df["close"] > 0).all()
