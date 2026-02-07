# Improvement suggestions (post–review)

This list comes from a full repository review after the release-readiness changes. Items are grouped by area and ordered by impact and effort where useful.

**Status:** All items below have been **executed** (branch `feature/release-readiness-improvements`). Source is under `src/` (renamed from `code/`). See `docs/PR-ITERATION1.md`, `docs/RELEASE_READINESS.md`, `docs/MIGRATION_CODE_TO_SRC.md`.

---

## 1. Code quality & consistency

### 1.1 Fix deprecated pandas API — **Done**
- **Where:** `src/integrated-strategy/utils.py` (multiple occurrences).
- **Issue:** `fillna(method='ffill')` is deprecated; use `ffill()` instead.
- **Action:** Replaced all `df.fillna(method='ffill')` with `df.ffill()`.

### 1.2 Consistent return formula — **Done**
- **Where:** `src/integrated-strategy/output-backtester.py`.
- **Issue:** Total return was divided by final value; should be relative to initial.
- **Action:** Now uses `(portfolio['total'].iloc[-1] - portfolio['total'].iloc[0]) / portfolio['total'].iloc[0]`.

### 1.3 Prefer `.iloc` for last/first elements — **Done**
- **Where:** `output-backtester.py`, `output-backtester_wrapper.py`, `baseline_wrapper.py`, `baseline.py`.
- **Action:** Refactored to `portfolio['total'].iloc[-1]` and `.iloc[0]` where touched.

---

## 2. Project structure & dependencies

### 2.1 Resolve `code/` vs stdlib name conflict — **Done**
- **Issue:** The top-level package name `code` shadows Python’s standard library `code` module, which forces `-p no:debugging` in pytest and can break other tools.
- **Action:** Renamed `code/` to `src/`. Updated README, tests, Cursor rules, docs. Migration note: `docs/MIGRATION_CODE_TO_SRC.md`.

### 2.2 Centralise data paths and make them configurable — **Done**
- **Action:** Added `src/config.py` with `DATA_ROOT`/`ALGOTRADING_DATA`, `get_price_path(symbol)`, `get_signals_path(symbol, base_dir)`, `safe_symbol(symbol)`. Used in `output-backtester_wrapper.py`, `baseline_wrapper.py`, `baseline.py`.

### 2.3 Optional dependencies as extras — **Done**
- **Where:** `requirements.txt`.
- **Issue:** Optional deps (torch, textblob, vaderSentiment, etc.) are commented; installing “integrated-strategy” or “paper-trading” deps is manual.
- **Action:** Added `requirements-integrated.txt`; documented in README.

---

## 3. Testing

### 3.1 Broader test coverage — **Done**
- **Action:** Added `tests/test_macd.py` (MACD signal shape, no NaNs). Added `tests/test_integration.py` (fixture CSV → Backtest → evaluate). Total: 14 tests (5 backtest, 6 evaluate, 2 MACD, 1 integration).

### 3.2 Integration test with fixture data — **Done**
- **Action:** Added `tests/fixtures/sample_prices.csv`, `sample_signals.csv`, and `test_backtest_with_fixture_csv` in `tests/test_integration.py`.

### 3.3 Regression test for return formula — **Done**
- **Action:** Added `test_backtest_return_formula` in `tests/test_backtest.py` (checks formula is well-defined and finite).

---

## 4. Security & robustness

### 4.1 Safe symbol and path handling everywhere — **Done**
- **Action:** Centralised `safe_symbol()` in `src/config.py`. Used in `output-backtester_wrapper.py`, `baseline_wrapper.py`, `baseline.py`. Paths via `get_price_path` / `get_signals_path`.

### 4.2 Paper-trading and IB configuration — **Done**
- **Where:** `src/paper-trading/main_reqMktData.py`.
- **Action:** Connection uses `IB_HOST`, `IB_PORT`, `IB_CLIENT_ID` from environment (defaults: 127.0.0.1, 7497, 0). Documented in README Data and environment section.

### 4.3 Graceful handling of missing data — **Done**
- **Where:** Scripts that call `pd.read_csv(...)` without try/except (e.g. many `main_*.py` in technical-analysis_python, `baseline.py`, filters).
- **Action:** Add try/except for `FileNotFoundError`/`OSError` and clear error messages (as in `output-backtester_wrapper.py`) so users see “file X not found” instead of a raw traceback.

---

## 5. Documentation

### 5.1 README table of contents — **Done**
- **Issue:** README has new sections (Requirements, Testing) but the Table of Contents at the top doesn’t list them.
- **Action:** TOC updated with Requirements, Testing, Data and environment.

### 5.2 Data layout and env vars — **Done**
- **Action:** README "Data and environment" section added (DATA_ROOT, IB_*, secrets, reproducibility).

### 5.3 CONTRIBUTING and development workflow — **Done**
- **Action:** Added `CONTRIBUTING.md` (run tests, add tests, code style, PR/docs, security).

### 5.4 Docstrings for key modules — **Done**
- **Action:** Module docstring in `src/evaluate.py`; `src/backtest.py` documents assumptions.

---

## 6. CI/CD and automation

### 6.1 Run tests on push/PR — **Done**
- **Action:** Added `.github/workflows/test.yml`: matrix Python 3.10/3.12, install from `requirements.txt`, run `pytest`.

### 6.2 Dependency and security checks — **Done**
- **Action:** Added `audit` job in same workflow running `pip audit` (continue-on-error: true).

---

## 7. Backtesting and research

### 7.1 Backtest engine enhancements (optional) — **Documented**
- **Action:** Assumptions documented in `src/backtest.py` module docstring (long-only, no commission/slippage, fixed 100 shares). No code change for parameterised size/commission.

### 7.2 Reproducibility for notebooks — **Done**
- **Where:** Many `.ipynb` in sentiment-analysis, macroeconomic-analysis, etc.
- **Action:** README "Data and environment" includes reproducibility note and reference to `src/integrated-strategy/README.md` for LSTM seeds.

---

## 8. Prioritised short list — **All complete**

1. ~~Fix deprecated `fillna`, return formula, README TOC~~ — **Done**
2. ~~Centralise data paths, safe symbol, CI~~ — **Done**
3. ~~Integration test, CONTRIBUTING.md, rename code/ to src/~~ — **Done**

---

*All items executed as of branch `feature/release-readiness-improvements`. Paths in this doc refer to `src/` (post-rename).*
