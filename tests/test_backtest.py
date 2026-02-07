"""
Smoke and unit tests for backtest module.
Run from repo root: python -m pytest tests/test_backtest.py -v
"""
import sys
from pathlib import Path

# Add code directory so we can import backtest and evaluate
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt

# Use non-interactive backend for CI/headless
import matplotlib
matplotlib.use("Agg")

from backtest import Backtest


def _make_price_df(index):
    """Price DataFrame with Close column."""
    n = len(index)
    return pd.DataFrame(
        {"Close": 100.0 + np.cumsum(np.random.randn(n).astype(np.float64) * 0.5)},
        index=index,
    )


def _make_signals(index, seed=42):
    """Signals DataFrame with 'signal' and 'positions'."""
    rng = np.random.default_rng(seed)
    signal = (rng.random(len(index)) > 0.5).astype(np.float64)
    signals = pd.DataFrame({"signal": signal}, index=index)
    signals["positions"] = signals["signal"].diff()
    return signals


def test_backtest_returns_portfolio_and_fig():
    """Smoke test: Backtest runs and returns portfolio DataFrame and figure."""
    dates = pd.date_range("2020-01-02", periods=100, freq="B")
    df = _make_price_df(dates)
    signals = _make_signals(dates)
    ticker = "TEST.HK"

    portfolio, fig = Backtest(ticker, signals, df, initial_capital=100000.0)

    assert isinstance(portfolio, pd.DataFrame)
    assert "total" in portfolio.columns
    assert "returns" in portfolio.columns
    assert "holdings" in portfolio.columns
    assert "cash" in portfolio.columns
    assert len(portfolio) == len(dates)
    assert fig is not None
    plt.close(fig)


def test_backtest_final_value_reasonable():
    """Final portfolio value is numeric and positive for normal inputs."""
    dates = pd.date_range("2019-01-01", periods=252, freq="B")
    df = _make_price_df(dates)
    signals = _make_signals(dates, seed=123)
    portfolio, fig = Backtest("X.HK", signals, df, initial_capital=100000.0)
    plt.close(fig)

    total = portfolio["total"].iloc[-1]
    assert np.isfinite(total)
    assert total > 0


def test_backtest_raises_on_no_common_index():
    """Backtest raises when signals and df have no common index."""
    dates_sig = pd.date_range("2020-01-01", periods=10, freq="B")
    dates_df = pd.date_range("2022-01-01", periods=10, freq="B")  # no overlap
    df = _make_price_df(dates_df)
    signals = _make_signals(dates_sig)
    with pytest.raises(ValueError, match="no common index"):
        Backtest("X.HK", signals, df)


def test_backtest_aligned_index_no_lookahead():
    """Backtest uses only common index (signals and prices aligned)."""
    dates = pd.date_range("2020-06-01", periods=50, freq="B")
    df = _make_price_df(dates)
    signals = _make_signals(dates)
    portfolio, fig = Backtest("A.HK", signals, df, initial_capital=50000.0)
    plt.close(fig)

    assert portfolio.index.equals(signals.index)


def test_backtest_return_formula():
    """Total return formula (final - initial) / initial is well-defined and finite."""
    dates = pd.date_range("2020-01-01", periods=20, freq="B")
    df = _make_price_df(dates)
    signals = _make_signals(dates, seed=99)
    portfolio, fig = Backtest("R.HK", signals, df, initial_capital=100000.0)
    plt.close(fig)

    initial = portfolio["total"].iloc[0]
    final = portfolio["total"].iloc[-1]
    assert initial > 0 and np.isfinite(final)
    return_pct = (final - initial) / initial * 100
    assert np.isfinite(return_pct)
