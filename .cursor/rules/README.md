# Cursor Rules (Review & Quality Hooks)

This folder defines **Cursor rules** that act as persistent "hooks" for repository review and quality. They are applied automatically when relevant.

## Iterative Review Hook (up to 20 iterations, min score 95)

- **Rule**: `iterative-review-and-grading.mdc`
- **Purpose**: When doing a full repo review or backtesting real-world readiness:
  - Grade the repo 0–100 on **real-world testing viability** (minimum **95** for backtesting).
  - Reiterate **up to 20 times**, each time doing:
    - **(a)** Review full project repository  
    - **(b)** Understand what has been done  
    - **(c)** Suggest improvements and changes  
    - **(d)** All changes as PR, clearly explained and documented  
    - **(e)** All changes tested and regression tested  
    - **(f)** Penetration / vulnerability awareness  
    - **(g)** Improve deprecated functions and upgrade to latest stable  
  - Stop when score ≥ 95 (for backtest/real-world) or after 20 iterations.

## Supporting Rules

- **`pr-and-documentation.mdc`**: Every change must be described as a PR with clear explanation and docs.
- **`testing-and-regression.mdc`**: All changes must be tested and regression tested (applies to `**/*.py`).
- **`security-and-deprecation.mdc`**: Security/vulnerability awareness and upgrading deprecated APIs to latest stable.

## How to trigger the full workflow

Ask Cursor to:

- "Run a full repository review and grade it for real-world backtesting; iterate until score ≥ 95 or 20 iterations."
- "Review the repo for release readiness using the iterative grading hook."

The agent will follow the iterative-review rule and the supporting rules for each iteration.
