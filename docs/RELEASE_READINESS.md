# Release readiness – iterative grading

This document records the **real-world backtesting viability** grade and iteration log from the Cursor iterative review hook (target: score ≥ 95, max 20 iterations).

---

## Grading rubric (100 pts)

| Category | Max | Description |
|----------|-----|-------------|
| Correctness | 10 | Backtest logic, no look-ahead, consistent indexing |
| Robustness | 15 | Error handling, missing data, edge cases |
| Reproducibility | 15 | Fixed seeds, documented data and versions |
| Safety | 15 | No hardcoded secrets, safe file/path handling |
| Testing | 20 | Automated tests and regression for critical paths |
| Documentation and PR | 10 | Clear PRs and docs |
| Dependencies and deprecations | 15 | Up-to-date, non-deprecated APIs |

---

## Iteration 1 – Summary (final score after follow-up fixes)

**Score: 95 / 100** ✓ (target reached)

| Category | Score | Notes |
|----------|-------|--------|
| Correctness | 10 | Index alignment in Backtest; raise on no common index; evaluate edge cases fixed. |
| Robustness | 14 | Backtest/evaluate hardened; output-backtester_wrapper has try/except and clear errors for missing CSV. |
| Reproducibility | 14 | requirements.txt; LSTM seeds and NumPy seed note in integrated-strategy README. |
| Safety | 14 | Safe symbol in output-backtester_wrapper; with open; README note on secrets. |
| Testing | 18 | 10 automated tests (backtest + evaluate), including edge-case tests. |
| Documentation and PR | 10 | README Requirements/Testing/Security; PR doc; pytest.ini; integrated-strategy reproducibility. |
| Dependencies and deprecations | 15 | requirements.txt; LSTM/numpy imports updated to use `np.newaxis` (no `from numpy import`). |

**Changes delivered:** See `docs/PR-ITERATION1.md`, plus: LSTM deprecation fixes, integrated-strategy README reproducibility note, output-backtester_wrapper error handling.

---

## Iteration 2 (optional)

To go further: *“Continue the release readiness review: implement the remaining items in RELEASE_READINESS.md and re-grade; iterate until score ≥ 95 or 20 iterations.”*
