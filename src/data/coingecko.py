from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import time
import pandas as pd

from src.utils.http import get_with_backoff
from src.utils.cache import read_json_cache, write_json_cache, is_fresh

BASE = "https://api.coingecko.com/api/v3"

def _build_df_from_payload(payload: Dict[str, Any]) -> pd.DataFrame:
    prices = payload.get("prices", [])
    vols   = payload.get("total_volumes", [])
    df_p = pd.DataFrame(prices, columns=["ms", "close"])
    df_v = pd.DataFrame(vols,   columns=["ms", "volume"])

    # (optional robustness) ensure numeric types
    df_p["close"]  = pd.to_numeric(df_p["close"], errors="coerce")
    df_v["volume"] = pd.to_numeric(df_v["volume"], errors="coerce")

    df = df_p.merge(df_v, on="ms", how="left")
    df["timestamp_utc"] = pd.to_datetime(df["ms"], unit="ms", utc=True)
    df["date"] = df["timestamp_utc"].dt.tz_convert("UTC").dt.date.astype("datetime64[ns]")
    df = df.drop(columns=["ms"]).sort_values("timestamp_utc").reset_index(drop=True)
    return df[["timestamp_utc","date","close","volume"]]

def fetch_daily_close_coin(
    coin_id: str,
    vs_currency: str = "usd",
    days: str = "max",
    cache_dir: str | Path = "data/raw/coingecko",
    ttl_seconds: int = 24*3600
) -> pd.DataFrame:
    """
    Returns daily ['timestamp_utc','date','close','volume'].
    Free tier: if time-range exceeded (error_code=10012), retry with days='365'
    regardless of whether 'days' was 'max' or a numeric >365.
    """
    cache_path = Path(cache_dir) / f"{coin_id}_{vs_currency}_{days}_market_chart.json"
    meta = read_json_cache(cache_path)
    if meta and is_fresh(meta, ttl_seconds):
        payload = meta
    else:
        params = {"vs_currency": vs_currency, "days": days, "interval": "daily"}
        status, payload = get_with_backoff(f"{BASE}/coins/{coin_id}/market_chart", params)

        # Robust free-tier fallback
        if status == 401 and isinstance(payload, dict):
            err = payload.get("error", {}).get("status", {})
            code = err.get("error_code")
            if code == 10012:
                # Cap to 365 and retry
                params["days"] = "365"
                status, payload = get_with_backoff(f"{BASE}/coins/{coin_id}/market_chart", params)

        if status != 200:
            raise RuntimeError(f"CoinGecko error {status}: {payload}")

        payload["_fetched_at"] = time.time()
        write_json_cache(cache_path, payload)

    return _build_df_from_payload(payload)

# ---- Day-3 helpers to align with pipeline expectations ----

def get_prices_daily(
    coin_id: str,
    vs: str = "usd",
    lookback_days: int | str = 365,
    cache_dir: str | Path = "data/raw/coingecko",
    ttl_seconds: int = 24*3600,
) -> pd.DataFrame:
    """
    Adapter: returns DAILY dataframe with index=date(UTC) and columns:
    ['open','high','low','close','vol','missing_hours'].

    Note: CoinGecko daily returns only close+volume.
    For transparency, set open=high=low=close for each day.
    """
    days_param = lookback_days if isinstance(lookback_days, str) else int(lookback_days)
    df = fetch_daily_close_coin(
        coin_id=coin_id,
        vs_currency=vs,
        days=str(days_param),
        cache_dir=cache_dir,
        ttl_seconds=ttl_seconds
    ).copy()

    # Normalize to canonical schema expected downstream
    df = (
        df.set_index(pd.to_datetime(df["date"], utc=True))
          .rename(columns={"volume": "vol"})
          .drop(columns=["date"])
    )
    df["open"] = df["close"]
    df["high"] = df["close"]
    df["low"]  = df["close"]
    df["missing_hours"] = df["close"].isna()

    df = df[["open", "high", "low", "close", "vol", "missing_hours"]]
    df.index.name = "date"
    return df.sort_index()

def save_parquet(df: pd.DataFrame, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p, index=True)
