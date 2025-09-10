# Crypto Index Bootcamp
FREE-first, reproducible digital-asset index research. Python 3.13; pinned deps; UTC-only timestamps.

## One-command rebuild (PowerShell)
```powershell
python -m src.pull_prices; python -m src.make_index; pytest


## Day 2 Rebuild (Windows)

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.\scripts\rebuild_day2.ps1


## Day 3 Quick Run
```powershell
.\.venv\Scripts\Activate.ps1
python -m src.data.make_prices
pytest -q
python -m src.data.make_index_csv
python -m src.data.plot_sanity
