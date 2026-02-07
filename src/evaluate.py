"""
Portfolio evaluation: return series, Sharpe ratio, max drawdown, CAGR, standard deviation.
All functions expect a portfolio DataFrame with 'returns' and 'total' columns (e.g. from backtest.Backtest).
"""
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def PortfolioReturn(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']

    # Create a figure
    fig = plt.figure()

    # Plot the results
    returns.plot(lw=1.2, label='Portfolio return')
    plt.legend()

    return fig

"""
Sharpe ratio
"""
def SharpeRatio(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']

    if (returns.std() != 0):
        # annualised Sharpe ratio
        sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    else:
        sharpe_ratio = 0
        
    return sharpe_ratio

"""
Maximum drawdown

:window: trailing 252 trading day window
"""
def MaxDrawdown(df, window=252):
    # Calculate the max drawdown in the past window days for each day 
    rolling_max = df['Close'].rolling(window, min_periods=1).max()
    daily_drawdown = df['Close'] / rolling_max - 1.0

    # Calculate the minimum (negative) daily drawdown
    max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

    # Create a figure
    fig = plt.figure()

    # Plot the results
    daily_drawdown.plot(lw=1.2, label='Daily drawdown')
    max_daily_drawdown.plot(lw=1.2, label='Max daily drawdown')
    plt.legend()

    return fig, max_daily_drawdown, daily_drawdown

"""
Compound Annual Growth Rate (CAGR)

Formula
-
(Ending value / Beginning value) ** (1/n) - 1
"""

def CAGR(portfolio):
    """Compound Annual Growth Rate. Requires at least 2 index points and positive initial total."""
    if len(portfolio) < 2:
        return 0.0
    days = (portfolio.index[-1] - portfolio.index[0]).days
    if days <= 0:
        return 0.0
    start_val = portfolio["total"].iloc[0]
    end_val = portfolio["total"].iloc[-1]
    if start_val <= 0 or not np.isfinite(end_val):
        return 0.0
    cagr = ((end_val / start_val) ** (252.0 / days)) - 1
    return cagr

"""
Standard Deviation (SD)

Formula
- 
sqrt(sum[(r_i - r_avg)^2] / n-1)
"""

def StandardDeviation(portfolio):
    """Annualized standard deviation of strategy returns. Returns 0 if fewer than 2 observations."""
    returns = portfolio["returns"]
    n = len(returns)
    if n < 2:
        return 0.0
    returns_diff = returns - returns.mean()
    returns_diff = returns_diff * returns_diff
    returns_diff_sum = returns_diff.sum()
    sd = math.sqrt(returns_diff_sum / (n - 1))
    return sd
