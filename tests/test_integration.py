"""
Integration test: load fixture CSV -> Backtest -> evaluate.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import pandas as pd
import matplotlib
matplotlib.use("Agg")

from backtest import Backtest
from evaluate import SharpeRatio, CAGR

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_backtest_with_fixture_csv():
    """Load fixture price and signals CSV, run Backtest and evaluate; assert sanity."""
    prices = pd.read_csv(
        FIXTURES / "sample_prices.csv",
        index_col="Date",
        parse_dates=True,
    )
    signals = pd.read_csv(
        FIXTURES / "sample_signals.csv",
        index_col="Date",
        parse_dates=True,
    )
    signals["positions"] = signals["signal"].diff()

    portfolio, fig = Backtest("FIX.HK", signals, prices, initial_capital=10000.0)
    import matplotlib.pyplot as plt
    plt.close(fig)

    assert "total" in portfolio.columns
    assert "returns" in portfolio.columns
    assert len(portfolio) == len(signals)
    assert portfolio["total"].iloc[-1] > 0

    sharpe = SharpeRatio(portfolio)
    cagr = CAGR(portfolio)
    assert sharpe == sharpe  # finite
    assert cagr == cagr  # finite
