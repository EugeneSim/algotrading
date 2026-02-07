# Contributing

Thanks for your interest in improving this repo. Below are minimal guidelines for development and pull requests.

## Running tests

From the repository root:

```bash
pip install -r requirements.txt
python -m pytest
```

Use `python -m pytest tests/ -v` for verbose output. The project uses `pytest.ini`; see README for pytest and source layout (project uses `src/`).

## Adding tests

- Place new tests under `tests/`, in files named `test_*.py`.
- For backtest and evaluation, ensure the test adds the `src` directory to `sys.path` so imports like `from backtest import Backtest` work, or rely on `tests/conftest.py`.
- Use a non-interactive matplotlib backend in tests (e.g. `matplotlib.use("Agg")`) and close figures in teardown to avoid warnings.

## Code style

- Prefer clear names and short functions. If the project adopts a formatter (e.g. Black) or linter (e.g. Ruff), run them before submitting.
- Document public functions and the module purpose (e.g. docstrings in `backtest.py`, `evaluate.py`, `config.py`).

## Pull requests and documentation

- Describe what changed and why in the PR description.
- Update README or relevant docs if you add options, env vars, or new entrypoints.
- Keep changes focused; split large refactors into smaller PRs when possible.

## Security

- Do not commit secrets or API keys. Use environment variables or config that is gitignored.
- Validate and sanitise inputs (e.g. symbols) when building file paths to avoid path traversal.
