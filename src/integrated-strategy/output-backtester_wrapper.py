import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
import os

sys.path.append("..")
sys.path.append("../technical-analysis_python/")
mpl.use("tkagg")  # issues with Big Sur

from config import get_price_path, get_signals_path, safe_symbol
from strategy.macd_crossover import macdCrossover
from backtest import Backtest
from evaluate import PortfolioReturn, SharpeRatio, MaxDrawdown, CAGR


def backtest(symbol):
    symbol = safe_symbol(symbol)
    price_file = get_price_path(symbol)

    # load price data
    try:
        df_whole = pd.read_csv(price_file, header=0, index_col="Date", parse_dates=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"Price file not found: {price_file}") from None
    except OSError as e:
        raise OSError(f"Could not read price file {price_file}: {e}") from e

    # select time range (for trading)
    #start = '2017-01-03'
    start = '2020-06-10'
    end = '2021-03-03'
    start_date = pd.Timestamp(start)
    end_date = pd.Timestamp(end)

    df = df_whole.loc[start_date:end_date]

    ticker = symbol + ".HK"

    # load signals csv (output from ML model)
    signals_dir = os.path.join(os.path.dirname(__file__), "LSTM_output_trend")
    signals_file = get_signals_path(symbol, signals_dir)

    try:
        signals = pd.read_csv(signals_file, header=0, index_col="Date", parse_dates=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"Signals file not found: {signals_file}") from None
    except OSError as e:
        raise OSError(f"Could not read signals file {signals_file}: {e}") from e
    signals['positions'] = signals['signal'].diff()
    signals = signals[~signals.index.duplicated(keep='first')]

    df = df[~df.index.duplicated(keep='first')]
    #print(signals.head())
    #print(df.head())

    """
    Backtesting & evaluation
    """
    portfolio, backtest_fig = Backtest(ticker, signals, df)
    plt.close()  # hide figure
    print("Final total value: {value:.4f} ".format(
            value=portfolio["total"].iloc[-1]))

    portfolio_return = (
        ((portfolio["total"].iloc[-1] - portfolio["total"].iloc[0]) / portfolio["total"].iloc[0]) * 100)
    print("Total return: {value:.4f}%".format(value=portfolio_return))

    trade_signals_num = len(signals[signals.positions == 1])
    print("No. of trade: {value}".format(
        value=trade_signals_num))


    """
    Plotting figures
    """
    backtest_fig.suptitle('Portfolio value', fontsize=14)
    #backtest_fig.savefig('./figures_LSTM-price-only/' + symbol + '-portfolio-value')
    #plt.show()

    # Evaluate strategy

    # 1. Portfolio return
    returns_fig = PortfolioReturn(portfolio)
    returns_fig.suptitle('Portfolio return')
    #returns_filename = './figures_LSTM-price-only/' + symbol + '-portfolo-return'
    #returns_fig.savefig(returns_filename)
    #plt.show()

    # 2. Sharpe ratio
    sharpe_ratio = SharpeRatio(portfolio)
    print("Sharpe ratio: {ratio:.4f} ".format(ratio=sharpe_ratio))

    # 3. Maximum drawdown
    maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
    maxDrawdown_fig.suptitle('Maximum drawdown', fontsize=14)
    #maxDrawdown_filename = './figures/' + symbol + '-LSTM_maximum-drawdown'
    #maxDrawdown_fig.savefig(maxDrawdown_filename)
    #plt.show()

    # 4. Compound Annual Growth Rate
    cagr = CAGR(portfolio)
    print("CAGR: {cagr:.4f} ".format(cagr=cagr))


    # Write to file
    with open("LSTM_trend_results_MACD.csv", "a", encoding="utf-8") as f:
        f.write(
            f"{ticker},{start},{end},{portfolio_return},{sharpe_ratio},{cagr},{trade_signals_num}\n"
        )

def main():
    ticker_list = ['0001', '0002', '0003', '0004', '0005', '0016', '0019', '0168', '0175', '0386', '0669', '0700',
                   '0762', '0823', '0857', '0868', '0883', '0939', '0941', '0968', '1211', '1299', '1818', '2319', '2382', '2688', '2689', '2899']

    #ticker_list = ['0001', '0002', '0003', '0004', '0005']

    for ticker in ticker_list:

        print("############ Ticker: " + ticker + " ############")
        backtest(ticker)
        print('\n')

if __name__ == "__main__":
    main()
