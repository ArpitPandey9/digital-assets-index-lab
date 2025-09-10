# src/data/plot_sanity.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    prices = pd.read_parquet("data/processed/btc_daily.parquet")
    idx = pd.read_csv("data/index/spot_bh_btc_base1000.csv", parse_dates=["date"]).set_index("date")

    Path("figures").mkdir(exist_ok=True)

    plt.figure()
    prices["close"].plot(title="BTC Close (USD)")
    plt.savefig("figures/btc_close.png", dpi=140, bbox_inches="tight")

    plt.figure()
    idx["index_level"].plot(title="BTC Buy-and-Hold Index (Base=1000)")
    plt.savefig("figures/btc_index_base1000.png", dpi=140, bbox_inches="tight")

if __name__ == "__main__":
    main()

