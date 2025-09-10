# src/data/make_prices.py
"""
Builds BTC/ETH daily parquet files (free-tier safe) and a merged parquet.

Outputs:
- data/processed/btc_daily.parquet
- data/processed/eth_daily.parquet
- data/processed/btc_eth_daily.parquet
"""

from pathlib import Path
from src.data.coingecko import get_prices_daily, save_parquet


def main() -> None:
    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)

    # Free-tier: cap to 365 days to avoid CoinGecko error_code=10012
    lookback_days = 365

    # Load daily BTC/ETH with canonical schema:
    # ['open','high','low','close','vol','missing_hours'] and UTC date index
    btc = get_prices_daily("bitcoin", "usd", lookback_days=lookback_days)
    eth = get_prices_daily("ethereum", "usd", lookback_days=lookback_days)

    # Save individual parquet files
    save_parquet(btc, out / "btc_daily.parquet")
    save_parquet(eth, out / "eth_daily.parquet")

    # Merge (inner join on date index) with column prefixes to prevent collisions
    merged = (
        btc.rename(columns=lambda c: f"btc_{c}")
           .join(eth.rename(columns=lambda c: f"eth_{c}"), how="inner")
    )

    merged.to_parquet(out / "btc_eth_daily.parquet")


if __name__ == "__main__":
    main()
