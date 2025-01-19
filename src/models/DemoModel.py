from backtesting import Strategy
from src.data.yFinanceData import get_ticker_data
from src.features.BacktestEngine import BacktestEngine

class SPYVIXStrategy(Strategy):
    def init(self):
        # Calculate VIX 20-day SMA using TA-Lib with the injected VIX data
        self.vix_data['SMA'] = talib.SMA(self.vix_data['Close'], timeperiod=21)
        # Calculate SPY's 20-day SMA using TA-Lib; note that self.I registers the indicator
        self.spy_sma20 = self.I(talib.SMA, self.data.Close, 20)

    def next(self):
        # Force an exit at the open of the bar if a position exists.
        if self.position:
            # We force a close based on the current bar’s Open.
            # Note: Orders will be executed at the next available price
            # and backtesting.py uses "open" of the next bar for pending orders.
            # However, to simulate an immediate exit at open,
            # we can close at the very start of this bar.
            # One typical workaround is to close immediately and treat that bar as the exit.
            self.position.close()
            # Optionally print a message for debugging:
            print(f"Exiting position at bar {self.data.index[-1]} (simulated open price exit)")
            # Return so we don't then open a new position on the same bar.
            return

        # Now, if no position, evaluate entry conditions.
        i = len(self.data) - 1
        vix_close = self.vix_data['Close'].iloc[i]
        vix_sma = self.vix_data['SMA'].iloc[i]

        if self.data.Close[-1] > self.spy_sma20[-1] and vix_close < vix_sma:
            print(f"Entering position at bar {self.data.index[-1]}")
            self.buy()

data = get_ticker_data("SPY",start="2010-01-01", end="2025-01-01")
bt = BacktestEngine(data,None,SPYVIXStrategy,10000,0.002)
results = bt.run()
for period in results:
    print()
    print("TRAIN PERIOD:", period['train_period'])
    print(period['train_results'])
    print()
    print("TEST PERIOD:", period['test_period'])
    print(period['test_results'])
    print("=" * 80)
    print()