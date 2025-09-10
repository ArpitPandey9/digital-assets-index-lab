# src/data/make_index_csv.py
import pandas as pd
from pathlib import Path

def bh_index_from_prices(df: pd.DataFrame, base: float = 1000.0) -> pd.DataFrame:
    """
    Build a base-1000 buy-and-hold index from a daily price dataframe.
    Expects df indexed by UTC daily datetime with a 'close' column.
    """
    ret = df["close"].pct_change().fillna(0.0)
    level = (1.0 + ret).cumprod() * base
    out = pd.DataFrame({"index_level": level})
    out.index.name = "date"
    out["divisor"] = base  # placeholder; keeps governance intent
    out["notes"] = ""
    return out

def main():
    prices_path = Path("data/processed/btc_daily.parquet")
    if not prices_path.exists():
        raise FileNotFoundError(f"Missing {prices_path}. Run: python -m src.data.make_prices")

    prices = pd.read_parquet(prices_path)

    idx = bh_index_from_prices(prices)
    outdir = Path("data/index")
    outdir.mkdir(parents=True, exist_ok=True)

    out = idx.reset_index()
    # enforce UTC + YYYY-MM-DD formatting for factsheets
    out["date"] = out["date"].dt.tz_convert("UTC").dt.strftime("%Y-%m-%d")
    out.to_csv(outdir / "spot_bh_btc_base1000.csv", index=False)

if __name__ == "__main__":
    main()
