# Digital Assets Index Lab
[![CI](https://img.shields.io/github/actions/workflow/status/ArpitPandey9/digital-assets-index-lab/ci.yml?label=CI)](https://github.com/ArpitPandey9/digital-assets-index-lab/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%7C3.11-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Lint: ruff](https://img.shields.io/badge/lint-ruff-46a)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-brightgreen)](https://arpitpandey9.github.io/digital-assets-index-lab/)

**Open, reproducible research in crypto/DeFi market prediction & digital-asset index design (free-first, leak-safe, audit-grade).**

---

## Quick Start (Windows PowerShell)

```powershell
# 1) Create & activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
python -m pip install -U pip
pip install -r requirements.txt  # use requirements.lock.txt with --require-hashes if you have it

# 3) First run: build prices → index → tests
python -m src.data.make_prices
python -m src.data.make_index_csv


python3 -m venv .venv
source .venv/bin/activate

python -m pip install -U pip
pip install -r requirements.txt  # or requirements.lock.txt with --require-hashes

python -m src.data.make_prices
python -m src.data.make_index_csv
pytest -q
python -m src.data.plot_sanity

.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.\scripts\rebuild_day2.ps1

.\.venv\Scripts\Activate.ps1
python -m src.data.make_prices
pytest -q
python -m src.data.make_index_csv
python -m src.data.plot_sanity

data/            # Parquet(zstd), snapshots, manifests
docs/            # rulebook, factsheets, methodology, mkdocs (optional)
figures/         # plots, charts
reports/         # auto-generated factsheets (PDF/HTML)
scripts/         # helper scripts (e.g., rebuild_day2.ps1)
src/             # package code (e.g., src/data/*.py, src/index/*.py)
tests/           # pytest suites (unit + golden fixtures)

pytest -q
python -m src.data.plot_sanity
