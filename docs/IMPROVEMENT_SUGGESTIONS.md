# Improvement suggestions (post–review)

This list comes from a full repository review after the release-readiness changes. Items are grouped by area and ordered by impact and effort where useful.

**Status:** All items below have been implemented (code renamed to `src/`, config module, tests, CI, docs, security, etc.). See PR/commits and this doc for reference.

---

## 1. Code quality & consistency

### 1.1 Fix deprecated pandas API
- **Where:** `code/integrated-strategy/utils.py` (multiple occurrences).
- **Issue:** `fillna(method='ffill')` is deprecated; use `ffill()` instead.
- **Action:** Replace all `df.fillna(method='ffill')` with `df.ffill()` (and same for `bfill` if any).

### 1.2 Consistent return formula
- **Where:** `code/integrated-strategy/output-backtester.py` (around line 50).
- **Issue:** Total return is computed as `(portfolio['total'][-1] - portfolio['total'][0]) / portfolio['total'][-1]`. Return should be relative to **initial** value, i.e. divide by `portfolio['total'][0]`.
- **Action:** Use `(portfolio['total'][-1] - portfolio['total'][0]) / portfolio['total'][0]` for consistency with `baseline_wrapper.py`, `output-backtester_wrapper.py`, and the rest of the repo.

### 1.3 Prefer `.iloc` for last/first elements
- **Where:** Various scripts (e.g. `portfolio['total'][-1]`, `portfolio['total'][0]`).
- **Issue:** Using `[-1]`/`[0]` on a Series can be ambiguous with a string index; `.iloc[-1]` and `.iloc[0]` are explicit and future-proof.
- **Action:** Optionally refactor to `portfolio['total'].iloc[-1]` and `portfolio['total'].iloc[0]` where you touch these lines (e.g. when fixing the return formula).

---

## 2. Project structure & dependencies

### 2.1 Resolve `code/` vs stdlib name conflict
- **Issue:** The top-level package name `code` shadows Python’s standard library `code` module, which forces `-p no:debugging` in pytest and can break other tools.
- **Action:** Consider renaming `code/` to something like `src/` or `algotrading/`, and update README, imports, and `sys.path` references. Document the change in a short migration note.

### 2.2 Centralise data paths and make them configurable
- **Issue:** Many scripts use hardcoded relative paths (`../../database/`, `database_real/`, `os.getcwd() + '/database/...'`). This makes it hard to run from different working directories or to point to different data roots.
- **Action:** Introduce a small config module or env-based convention (e.g. `DATA_ROOT` or `ALGOTRADING_DATA`) and helper functions like `get_price_path(symbol)` / `get_signals_path(symbol)` that resolve under that root. Use it in integrated-strategy, technical-analysis_python, and filters.

### 2.3 Optional dependencies as extras
- **Where:** `requirements.txt`.
- **Issue:** Optional deps (torch, textblob, vaderSentiment, etc.) are commented; installing “integrated-strategy” or “paper-trading” deps is manual.
- **Action:** Add optional extras, e.g. `pip install -e ".[integrated]"` or a second file `requirements-integrated.txt`, and document in README.

---

## 3. Testing

### 3.1 Broader test coverage
- **Current:** 10 tests for `backtest` and `evaluate` only.
- **Action:** Add tests for:
  - **Technical indicators:** At least one strategy (e.g. MACD) in `technical-analysis_python/strategy/`: signal shape, no NaNs where not expected.
  - **Integrated-strategy:** A minimal smoke test that mocks or uses tiny CSVs and runs one backtest path (e.g. `output_backtester_wrapper.backtest` with safe symbol and fixture data) to avoid regressions.

### 3.2 Integration test with fixture data
- **Issue:** No test runs the full pipeline (load CSV → Backtest → evaluate) with a small fixture file.
- **Action:** Add a small CSV under `tests/fixtures/` (or `tests/data/`) and a test that loads it, runs `Backtest` and one or two evaluate functions, and asserts on column presence and basic sanity (e.g. final total > 0).

### 3.3 Regression test for return formula
- **Action:** Add a test that checks total return is `(final - initial) / initial` (e.g. for a known signal/price series with a known expected return).

---

## 4. Security & robustness

### 4.1 Safe symbol and path handling everywhere
- **Current:** `_safe_symbol()` exists only in `output-backtester_wrapper.py`.
- **Action:** Reuse or replicate symbol validation (alphanumeric only) and safe path construction in `baseline_wrapper.py`, `baseline.py`, and any script that builds file paths from user or list-driven symbols. Avoid path traversal (e.g. symbol `../../../etc/passwd`).

### 4.2 Paper-trading and IB configuration
- **Where:** `code/paper-trading/` (e.g. `main_reqMktData.py`: host `127.0.0.1`, port `7497`).
- **Action:** Read host/port from environment (e.g. `IB_HOST`, `IB_PORT`) with sensible defaults, and document in README so credentials and connection details are not hardcoded.

### 4.3 Graceful handling of missing data
- **Where:** Scripts that call `pd.read_csv(...)` without try/except (e.g. many `main_*.py` in technical-analysis_python, `baseline.py`, filters).
- **Action:** Add try/except for `FileNotFoundError`/`OSError` and clear error messages (as in `output-backtester_wrapper.py`) so users see “file X not found” instead of a raw traceback.

---

## 5. Documentation

### 5.1 README table of contents
- **Issue:** README has new sections (Requirements, Testing) but the Table of Contents at the top doesn’t list them.
- **Action:** Add “Requirements” and “Testing” (and “Security” if you add a short subsection) to the TOC and link to the right anchors.

### 5.2 Data layout and env vars
- **Action:** Add a short “Data and environment” (or “Configuration”) section: where to put data (e.g. `database/` vs `database_real/`), which env vars are used (e.g. `DATA_ROOT`, `IB_HOST`, `IB_PORT`), and that API keys/secrets must not be committed.

### 5.3 CONTRIBUTING and development workflow
- **Issue:** No CONTRIBUTING.md or similar.
- **Action:** Add a short CONTRIBUTING.md: how to run tests, how to add a test, code style (e.g. Black/isort if you adopt them), and that changes should be documented (e.g. PR description or release notes).

### 5.4 Docstrings for key modules
- **Action:** Ensure `evaluate.py` and any other public modules have a module-level docstring and that public functions have at least a one-line description (you’ve already improved `backtest.py` and parts of `evaluate.py`; extend to strategy/indicator modules if they’re part of the “public” API).

---

## 6. CI/CD and automation

### 6.1 Run tests on push/PR
- **Issue:** No GitHub Actions (or other CI) config found.
- **Action:** Add a workflow (e.g. `.github/workflows/test.yml`) that installs deps from `requirements.txt`, runs `python -m pytest`, and optionally runs on a few Python versions (e.g. 3.10, 3.12). Use the same pytest options as locally (e.g. from `pytest.ini`, including `-p no:debugging` if the `code/` name is unchanged).

### 6.2 Dependency and security checks
- **Action:** Add a job or scheduled run that executes `pip audit` (or `safety check`) and fails on known vulnerabilities; optionally Dependabot for dependency updates.

---

## 7. Backtesting and research

### 7.1 Backtest engine enhancements (optional)
- **Current:** Fixed 100 shares, long-only.
- **Ideas:** Parameterise position size (e.g. by capital or volatility), optional commission/slippage, and support for multiple symbols if you extend the strategy layer. Document assumptions (e.g. no shorting, no fees) in docstrings.

### 7.2 Reproducibility for notebooks
- **Where:** Many `.ipynb` in sentiment-analysis, macroeconomic-analysis, etc.
- **Action:** Where they use randomness, add a cell that sets `np.random.seed(...)` and document “run top to bottom for reproducible results.” Optionally run key notebooks in CI (e.g. with `jupyter nbconvert --execute` and a small dataset).

---

## 8. Prioritised short list

If you want to tackle a few items first:

1. **High impact, low effort:** Fix deprecated `fillna(method='ffill')` in `utils.py`; fix return formula in `output-backtester.py`; add Requirements/Testing to README TOC.
2. **High impact, medium effort:** Centralise data paths (config or env); add safe symbol/path handling to baseline and any script that builds paths from symbols; add CI that runs pytest.
3. **Quality and maintainability:** Add one integration test with fixture CSV; add CONTRIBUTING.md; consider renaming `code/` to avoid stdlib conflict.

---

*Generated from a full repository review. You can tick off items as you implement them or move them to a roadmap.*
