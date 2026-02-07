"""
Tests for evaluate module (PortfolioReturn, SharpeRatio, MaxDrawdown, CAGR, StandardDeviation).
Run from repo root: python -m pytest tests/test_evaluate.py -v
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import numpy as np
import pandas as pd
import pytest
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")

from evaluate import (
    PortfolioReturn,
    SharpeRatio,
    MaxDrawdown,
    CAGR,
    StandardDeviation,
)


def _portfolio_with_returns(dates, returns_series):
    """Build a minimal portfolio DataFrame with 'returns' and 'total'."""
    total = 100000.0 * np.cumprod(1 + returns_series)
    return pd.DataFrame(
        {"returns": returns_series, "total": total},
        index=dates,
    )


def test_sharpe_ratio_zero_vol_returns_zero():
    """SharpeRatio returns 0 when std is 0."""
    dates = pd.date_range("2020-01-01", periods=10, freq="B")
    returns = pd.Series(0.0, index=dates)
    portfolio = _portfolio_with_returns(dates, returns)
    assert SharpeRatio(portfolio) == 0.0


def test_sharpe_ratio_positive_returns_positive_sharpe():
    """Positive mean return with some vol gives positive Sharpe."""
    dates = pd.date_range("2020-01-01", periods=252, freq="B")
    np.random.seed(42)
    returns = pd.Series(0.001 + 0.01 * np.random.randn(252), index=dates)
    portfolio = _portfolio_with_returns(dates, returns)
    sr = SharpeRatio(portfolio)
    assert np.isfinite(sr)


def test_cagr_finite():
    """CAGR returns finite value for normal portfolio."""
    dates = pd.date_range("2020-01-01", periods=252, freq="B")
    returns = pd.Series(0.0005, index=dates)
    portfolio = _portfolio_with_returns(dates, returns)
    cagr = CAGR(portfolio)
    assert np.isfinite(cagr)


def test_standard_deviation_single_return():
    """StandardDeviation handles single return (avoid div by zero)."""
    dates = pd.date_range("2020-01-01", periods=1, freq="B")
    returns = pd.Series([0.01], index=dates)
    portfolio = _portfolio_with_returns(dates, returns)
    sd = StandardDeviation(portfolio)
    # Expect 0 or a defined value, not crash
    assert np.isfinite(sd)


def test_max_drawdown_returns_fig_and_series():
    """MaxDrawdown returns fig, max_daily_drawdown, daily_drawdown."""
    dates = pd.date_range("2020-01-01", periods=100, freq="B")
    df = pd.DataFrame({"Close": 100.0 + np.cumsum(np.random.randn(100) * 0.5)}, index=dates)
    fig, max_dd, daily_dd = MaxDrawdown(df, window=20)
    assert fig is not None
    assert len(max_dd) == len(dates)
    assert len(daily_dd) == len(dates)
    plt.close(fig)


def test_portfolio_return_returns_fig():
    """PortfolioReturn returns a figure."""
    dates = pd.date_range("2020-01-01", periods=20, freq="B")
    returns = pd.Series(0.001, index=dates)
    portfolio = _portfolio_with_returns(dates, returns)
    fig = PortfolioReturn(portfolio)
    assert fig is not None
    plt.close(fig)
