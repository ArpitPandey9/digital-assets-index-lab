# digital-assets-index-lab
Free-first, reproducible crypto/DeFi prediction & index research with purged CV, PBO, VaR/ES backtests, and S&P-style factsheets.

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
