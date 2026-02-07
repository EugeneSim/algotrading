# Migration: `code/` renamed to `src/`

The top-level directory that contained all Python modules and notebooks was renamed from **`code/`** to **`src/`** to avoid shadowing Python’s standard library `code` module (which broke pytest’s debugging plugin and could affect other tools).

## What changed

- **Directory:** `code/` → `src/`. All contents (e.g. `backtest.py`, `evaluate.py`, `integrated-strategy/`, `technical-analysis_python/`, etc.) now live under `src/`.
- **Imports and paths:** Scripts that do `sys.path.append("..")` from inside a subfolder of the repo still work, because `..` now points to `src/` (the parent of e.g. `src/integrated-strategy`). Tests use `ROOT / "src"` in `conftest.py` and in each test file.
- **README and docs:** References to “the `/code` directory” were updated to “the `/src` directory”. Optional pytest flag `-p no:debugging` is no longer strictly required when running from a checkout that uses `src/`, but it remains in `pytest.ini` for compatibility.

## What you need to do

- If you have bookmarks or scripts that point at `code/`, update them to `src/`.
- If you added the repo as a package with `sys.path` or `PYTHONPATH` pointing at `code/`, point it at `src/` instead.
- No changes are required inside the repo’s Python files for the rename; paths relative to the package root were updated in the same commit.
