# scripts/audit_day3.py
from __future__ import annotations
import sys, os, hashlib, textwrap
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
out = []

def h(msg=""):
    out.append(msg)

def sha256_file(p: Path) -> str:
    if not p.exists():
        return "MISSING"
    hsh = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hsh.update(chunk)
    return hsh.hexdigest()[:16]

def check_exists(p: Path, label: str) -> bool:
    ok = p.exists()
    h(f"[{'PASS' if ok else 'FAIL'}] exists: {label} -> {p}")
    return ok

def preview_parquet(p: Path, n=5):
    df = pd.read_parquet(p)
    h(f"shape={df.shape}, index.name={df.index.name}, tz={(getattr(df.index, 'tz', None))}")
    h(df.head(n).to_string())

def preview_csv(p: Path, n=10):
    df = pd.read_csv(p)
    h(f"shape={df.shape}")
    h(df.head(n).to_string())
    return df

def rule(assertion: bool, msg: str):
    h(f"[{'PASS' if assertion else 'FAIL'}] {msg}")
    return assertion

def main():
    h("# Day-3 Audit Report")
    h(f"Project root: {ROOT}")

    # 1) Required files
    files = {
        "README": ROOT / "README.md",
        "DATA_DICTIONARY": ROOT / "docs" / "DATA_DICTIONARY.md",
        "BTC parquet": ROOT / "data" / "processed" / "btc_daily.parquet",
        "ETH parquet": ROOT / "data" / "processed" / "eth_daily.parquet",
        "Merged parquet": ROOT / "data" / "processed" / "btc_eth_daily.parquet",
        "Index CSV": ROOT / "data" / "index" / "spot_bh_btc_base1000.csv",
        "Plot 1": ROOT / "figures" / "btc_close.png",
        "Plot 2": ROOT / "figures" / "btc_index_base1000.png",
        "Loader": ROOT / "src" / "data" / "coingecko.py",
        "Make prices": ROOT / "src" / "data" / "make_prices.py",
        "Make index": ROOT / "src" / "data" / "make_index_csv.py",
        "Plot script": ROOT / "src" / "data" / "plot_sanity.py",
        "Tests": ROOT / "tests" / "test_coingecko.py",
    }

    all_exist = True
    for label, p in files.items():
        ok = check_exists(p, label)
        all_exist = all_exist and ok

    # 2) Previews + schema checks
    if files["BTC parquet"].exists():
        h("\n## BTC parquet preview")
        preview_parquet(files["BTC parquet"])
        df_btc = pd.read_parquet(files["BTC parquet"])
        exp_cols = {"open","high","low","close","vol","missing_hours"}
        rule(exp_cols.issubset(set(df_btc.columns)), "BTC columns include open/high/low/close/vol/missing_hours")
        rule(getattr(df_btc.index, "tz", None) is not None, "BTC index is timezone-aware (UTC expected)")
        rule(len(df_btc) >= 360, "BTC has at least ~360 rows (last 365 days)")

    if files["ETH parquet"].exists():
        h("\n## ETH parquet preview")
        preview_parquet(files["ETH parquet"])
        df_eth = pd.read_parquet(files["ETH parquet"])
        exp_cols = {"open","high","low","close","vol","missing_hours"}
        rule(exp_cols.issubset(set(df_eth.columns)), "ETH columns include open/high/low/close/vol/missing_hours")
        rule(getattr(df_eth.index, "tz", None) is not None, "ETH index is timezone-aware (UTC expected)")
        rule(len(df_eth) >= 360, "ETH has at least ~360 rows (last 365 days)")

    if files["Merged parquet"].exists():
        h("\n## Merged parquet preview")
        preview_parquet(files["Merged parquet"])
        df_m = pd.read_parquet(files["Merged parquet"])
        exp_pref = {"btc_", "eth_"}
        rule(all(any(c.startswith(pfx) for c in df_m.columns) for pfx in exp_pref),
             "Merged columns are prefixed with btc_/eth_")
        rule(len(df_m) >= 350, "Merged has at least ~350 rows (intersection)")

    # 3) Index CSV checks
    if files["Index CSV"].exists():
        h("\n## Index CSV preview")
        df_idx = preview_csv(files["Index CSV"], n=10)
        # Rules: starts at ~1000, dates monotonic
        try:
            starts_at = float(df_idx.loc[0, "index_level"])
        except Exception:
            starts_at = None
        rule(starts_at is not None and abs(starts_at - 1000.0) < 1e-6, "Index starts at 1000.0 on first date")
        # monotonic dates
        rule(pd.to_datetime(df_idx["date"]).is_monotonic_increasing, "Index dates strictly increasing")
        # required cols
        rule({"date","index_level","divisor","notes"}.issubset(set(df_idx.columns)),
             "Index CSV has required columns (date, index_level, divisor, notes)")

    # 4) Hash quick fingerprints for reproducibility
    h("\n## File fingerprints (sha256, first 16 hex)")
    for label, p in files.items():
        if p.exists():
            h(f"{label:16s} {sha256_file(p)}")

    # 5) Save + print
    report_path = REPORTS / "day3_audit.txt"
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote audit report to {report_path}")
    print("\n" + "\n".join(out[:200]))  # print beginning of report for quick view

if __name__ == "__main__":
    sys.exit(main())
