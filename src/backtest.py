"""
Backtest engine: simulates a simple long-only strategy from signals and price data.
Uses common index of signals and prices to avoid look-ahead bias.

Assumptions: long-only (no shorting), no commission or slippage, fixed 100 shares per trade.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def Backtest(ticker, signals, df, initial_capital=float(100000.0)):
    """
    Run backtest: long-only, fixed 100 shares per signal.

    Parameters
    ----------
    ticker : str
        Symbol name (e.g. '0001.HK').
    signals : pd.DataFrame
        Must have DatetimeIndex, columns 'signal' (0/1) and 'positions' (from signal.diff()).
    df : pd.DataFrame
        Price data with DatetimeIndex and 'Close' column.
    initial_capital : float
        Starting cash.

    Returns
    -------
    portfolio : pd.DataFrame
        Columns: ticker, holdings, cash, total, returns.
    fig : matplotlib.figure.Figure
        Equity curve figure.
    """
    # Align to common index to avoid look-ahead and NaNs
    common_idx = signals.index.intersection(df.index).sort_values()
    if len(common_idx) == 0:
        raise ValueError("signals and df have no common index; cannot run backtest")
    signals = signals.reindex(common_idx).ffill().fillna(0.0)
    df = df.reindex(common_idx).ffill().bfill()

    positions = pd.DataFrame(index=common_idx).fillna(0.0)
    positions[ticker] = 100 * signals["signal"]

    portfolio = positions.multiply(df["Close"], axis=0)

    # Store the difference in shares owned 
    pos_diff = positions.diff()

    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(df['Close'], axis=0)).sum(axis=1)

    # Add `cash` to portfolio
    portfolio['cash'] = initial_capital - (pos_diff.multiply(df['Close'], axis=0)).sum(axis=1).cumsum()   

    # Add `total` to portfolio
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']

    # Add `returns` to portfolio
    portfolio['returns'] = portfolio['total'].pct_change()

    # Plot portfolio value

    # Create a figure
    fig = plt.figure(figsize=(8, 6))
    fig.set_size_inches(8, 6)

    ax1 = fig.add_subplot(111, ylabel="Portfolio value in $")

    # Plot the equity curve and markers with the same axis (avoids converter warning)
    ax1.plot(
        portfolio.index,
        portfolio["total"].values,
        lw=1.2,
        label="Total value (including cash)",
    )
    buy_mask = signals["positions"] == 1.0
    sell_mask = signals["positions"] == -1.0
    ax1.plot(
        portfolio.loc[buy_mask].index,
        portfolio["total"].loc[buy_mask].values,
        "^",
        markersize=8,
        color="g",
        label="Buy signal",
    )
    ax1.plot(
        portfolio.loc[sell_mask].index,
        portfolio["total"].loc[sell_mask].values,
        "v",
        markersize=8,
        color="r",
        label="Sell signal",
    )

    plt.legend()
    
    return portfolio, fig
