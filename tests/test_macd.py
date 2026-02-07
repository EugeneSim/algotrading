"""
Tests for MACD crossover strategy (technical-analysis_python).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TA_PY = SRC / "technical-analysis_python"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(TA_PY))

import numpy as np
import pandas as pd
import pytest
import matplotlib
matplotlib.use("Agg")

from strategy.macd_crossover import macdCrossover


def _make_price_df(index):
    n = len(index)
    return pd.DataFrame(
        {"Close": 100.0 + np.cumsum(np.random.default_rng(42).random(n) * 2 - 1)},
        index=index,
    )


def test_macd_gen_signals_shape_and_columns():
    """MACD gen_signals returns DataFrame with signal and positions, same index as df."""
    dates = pd.date_range("2020-01-01", periods=100, freq="B")
    df = _make_price_df(dates)
    macd = macdCrossover(df)
    macd.plot_MACD()
    signals = macd.gen_signals()

    assert isinstance(signals, pd.DataFrame)
    assert "signal" in signals.columns
    assert "positions" in signals.columns
    assert len(signals) == len(dates)
    assert signals.index.equals(df.index)


def test_macd_signals_no_nan_in_signal():
    """MACD signal column has no NaN after gen_signals (positions may have first NaN)."""
    dates = pd.date_range("2019-06-01", periods=50, freq="B")
    df = _make_price_df(dates)
    macd = macdCrossover(df)
    macd.plot_MACD()
    signals = macd.gen_signals()

    assert signals["signal"].notna().all()
    assert signals["signal"].isin([0.0, 1.0]).all()
