# Day 3 Data Dictionary

## Processed Parquet Files

**data/processed/btc_daily.parquet**
- Index: `date` (UTC daily)
- Columns:
  - `open`, `high`, `low`, `close` (float, USD)
  - `vol` (float, raw volume from CoinGecko)
  - `missing_hours` (bool)

**data/processed/eth_daily.parquet**
- Same schema as BTC parquet, but for Ethereum.

**data/processed/btc_eth_daily.parquet**
- Index: `date` (UTC daily)
- Columns:
  - `btc_open`, `btc_high`, `btc_low`, `btc_close`, `btc_vol`, `btc_missing_hours`
  - `eth_open`, `eth_high`, `eth_low`, `eth_close`, `eth_vol`, `eth_missing_hours`

## Index CSV

**data/index/spot_bh_btc_base1000.csv**
- `date` (YYYY-MM-DD, UTC)
- `index_level` (float, base = 1000.0 at first date)
- `divisor` (float, placeholder for governance; fixed at 1000.0 here)
- `notes` (string, empty or flags)
