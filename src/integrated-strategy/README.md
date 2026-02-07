## Integrated Strategy
The following strategies have been implemented in Python:

### Reproducibility
For reproducible LSTM training, seeds are set in the scripts (e.g. `torch.manual_seed(1)` in `LSTM-train_wrapper.py` and `LSTM-train_daily.py`). To fix NumPy randomness as well, set `np.random.seed(42)` (or another value) at the start of the training script. DataLoader shuffle is set to `False` in these scripts to avoid non-determinism.

#### Baseline model
* `baseline.py` (for one ticker)
* `baseline_wrapper.py` (for a set of tickers)
  
#### Single-feature LSTM model 
* `LSTM-train_price-only.py` (for one ticker)
* `LSTM-train_price-only_wrapper.py` (for a set of tickers)

#### Multi-feature LSTM model
* `LSTM-train_wrapper.py` (for a set of tickers)

#### Multi-feature LSTM model with paper trading in IB
* `LSTM-train_daily.py` (for training the model)
* `daily_trading_strategy.py` (for generating the daily trading signal)
* `daily_trading_order.py` (for making the order via IB)