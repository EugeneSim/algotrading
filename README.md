![CC0-1.0 License][license-shield] 
![Last commit][last-commit-shield]
![Language][language-shield]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <img src="images/logo.png" alt="Logo" width="80" height="80">
  <h3 align="center">Algorithmic trading learning repo</h3>

  <p align="center">
    This repo features code and tutorials for beginners to learn algo trading.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About this repo](#-about-this-repo)
* [How to use](#-how-to-use)
* [Code overview](#-code-overview)
* [Requirements](#-requirements)
* [Testing](#-testing)
* [Data and environment](#-data-and-environment)
* [Development](#-development)
* [Contact](#-contact)
* [Acknowledgements](#-acknowledgements)
* [License](#%EF%B8%8F-license)

## 💻 About this repo 

This repo is built as part of the Final Year Project (FYP) at the Department of Computer Science of The University of Hong Kong (HKU). 

## 🤔 How to use

All the code could be found in the `/src` directory and the documentation could be accessed at [https://algo-trading.readthedocs.io/](https://algo-trading.readthedocs.io/).

(Note that the `/database` directory only contains example files. The actual database is stored in the HKU Department of Computer Science server.)  

## 📁 Code overview

### 1. Introduction
`intro-to-algotrading/`
* Basic data science
* Data scrapping


### 2. Technical Analysis
`technical-analysis_basics/`
* Chart analysis
* Trend analysis
* Basics of technical analysis

`technical-analysis_python/`
* Technical indicators implementation

`technical-analysis_julia/`
* Moving Average strategy implementation


### 3. Fundamental Analysis
`fundamental-analysis/`
* Ratio analysis & stock screening

`bankruptcy-prediction/`
* Prediction with machine learning models

### 4. Macroeconomic Analysis
`macroeconomic-analysis/`
* Property transaction data scrapping
* Property transaction data analysis
* Macroeconomic indicators analysis
* Property price prediction

### 5. Sentiment Analysis
`sentiment-analysis/`
* News data collection
* Tweets data collection
* VADER sentiment analysis
* Textblob sentiment analysis

### 6. Trade Execution
`paper-trading/`
* Paper Trading using Interactive Brokers (IB)

### 7. Integrated Strategies
`integrated-strategy/`
* Baseline model with data filters
* Trading signal generation with LSTM (single-feature)
* Trading signal generation with LSTM (multi-feature)
* Daily trading signal generation with LSTM + trade execution with IB


## 📦 Requirements

Install core dependencies for the backtest and evaluation stack:

```bash
pip install -r requirements.txt
```

See `requirements.txt` for version ranges. Optional dependencies (e.g. for integrated-strategy or paper-trading) are commented there. Do not commit API keys or secrets; use environment variables or config files that are listed in `.gitignore`.

## 🧪 Testing

Automated tests for the backtest and evaluation modules live in `/tests`. Run them from the repo root:

```bash
python -m pytest
```

Or explicitly: `python -m pytest tests/ -v -p no:debugging`. The config in `pytest.ini` disables the debugging plugin to avoid a naming conflict between this repo’s `code/` package and Python’s standard library `code` module. All tests use a non-interactive matplotlib backend.

Optional dependencies (integrated-strategy, paper-trading): `pip install -r requirements-integrated.txt` (installs base requirements plus torch, textblob, vaderSentiment, etc.).

## 📂 Data and environment

- **Data layout:** Price and example data live under `/database`. Some scripts expect a separate `database_real/` (e.g. full HKEX data, macro determinants) for LSTM and filters; that path is in `.gitignore`. Override the data root with the **`DATA_ROOT`** or **`ALGOTRADING_DATA`** environment variable so scripts can find CSVs when run from any working directory.
- **Paper trading (IB):** Set **`IB_HOST`**, **`IB_PORT`**, and optionally **`IB_CLIENT_ID`** (defaults: `127.0.0.1`, `7497`, `0`) so connection details are not hardcoded.
- **Secrets:** Do not commit API keys or passwords. Use environment variables or config files that are listed in `.gitignore`.

- **Reproducibility (notebooks):** For reproducible results in Jupyter notebooks, set `np.random.seed(42)` (or another value) in a cell before any random operations and run cells from top to bottom. LSTM training scripts use `torch.manual_seed(1)`; see `src/integrated-strategy/README.md`.

## 🔧 Development

The source code of the Sphinx documentation website could be found in the `/docs` directory. After updating any of the `*.rst` files in `/docs/source/`, run the following to generate the HTML files:

```
make html
```

## 📮 Contact

Project Link: https://awoo424.github.io/algotrading_fyp/

## 📚 Acknowledgements

* [Investopedia](https://www.investopedia.com/)
* [StockCharts](https://stockcharts.com/)
* [Technical Analysis Library in Python](https://github.com/bukosabino/ta) 

## ⚖️ License
Licensed under the Creative Commons Zero v1.0 Universal.
[Copy of the license](https://github.com/awoo424/algotrading/blob/master/LICENSE).

<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/awoo424/algotrading
[last-commit-shield]: https://img.shields.io/github/last-commit/awoo424/algotrading?color=blue
[language-shield]: https://img.shields.io/github/languages/top/awoo424/algotrading?color=purple
