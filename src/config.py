"""
Centralised configuration for data paths and optional settings.
Uses environment variable DATA_ROOT (or ALGOTRADING_DATA) for the repo/data root;
defaults to the parent of the directory containing this file, then 'database'.
"""
import os
import re

# Repo root: parent of code/ (or src/). Data root: DATA_ROOT or repo/database.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_DATA_ROOT = os.environ.get("DATA_ROOT") or os.environ.get("ALGOTRADING_DATA") or os.path.join(_REPO_ROOT, "database")
_DATABASE_REAL = os.path.join(_REPO_ROOT, "database_real")


def get_data_root():
    """Return the data root directory (database or override via env)."""
    return _DATA_ROOT


def get_database_real_root():
    """Return the database_real directory path (may not exist)."""
    return _DATABASE_REAL


def _safe_symbol(symbol: str) -> str:
    """Allow only alphanumeric symbols to avoid path traversal."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol must be a non-empty string")
    if not re.match(r"^[a-zA-Z0-9]+$", symbol):
        raise ValueError("symbol must contain only alphanumeric characters")
    return symbol


# Public alias for use in other modules
safe_symbol = _safe_symbol


def get_price_path(symbol: str, subdir: str = "microeconomic_data/hkex_ticks_day") -> str:
    """
    Return path to price CSV for a symbol under data root.
    symbol: e.g. '0001' (no .HK). Validated for alphanumeric only.
    """
    safe = _safe_symbol(symbol)
    return os.path.join(_DATA_ROOT, subdir, f"hkex_{safe}.csv")


def get_signals_path(symbol: str, base_dir: str) -> str:
    """
    Return path to signals CSV for a symbol under base_dir (e.g. LSTM_output_trend).
    base_dir can be relative to cwd or absolute.
    """
    safe = _safe_symbol(symbol)
    return os.path.join(base_dir, f"{safe}_output.csv")


def get_sentiment_scores_path(ticker: str) -> str:
    """Return path to sentiment scores CSV under data root (e.g. sentiment-scores/0001.HK.csv)."""
    # ticker may be 0001.HK; we need a safe filename part
    base = ticker.split(".")[0] if "." in ticker else ticker
    safe = _safe_symbol(base)
    return os.path.join(_DATA_ROOT, "sentiment_data", "sentiment-scores", f"{safe}.HK.csv")
