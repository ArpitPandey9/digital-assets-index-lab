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


[![CI](https://img.shields.io/github/actions/workflow/status/ArpitPandey9/digital-assets-index-lab/ci.yml?label=CI)](https://github.com/ArpitPandey9/digital-assets-index-lab/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%7C3.11-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Lint: ruff](https://img.shields.io/badge/lint-ruff-46a)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-brightgreen)](https://arpitpandey9.github.io/digital-assets-index-lab/)
