import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class CumulativeRSIStrategy(Strategy):
    # Define any strategy parameters if needed
    def init(self):
        # Initialize indicators using self.I
        # self.I registers the indicator with backtesting.py for optimized calculations

        # 200-day Simple Moving Average
        self.sma_200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

        # 3-day RSI
        self.rsi_3 = self.I(talib.RSI, self.data.Close, timeperiod=3)

        # 2-day Cumulative RSI (Sum of last 2 days' 3-day RSI)
        # Define a custom function for cumulative RSI
        self.cumulative_rsi_2 = self.I(lambda x: talib.SUM(x, timeperiod=2), self.rsi_3)

        # 2-day RSI for exit condition
        self.rsi_2 = self.I(talib.RSI, self.data.Close, timeperiod=2)

    def next(self):
        # Entry Condition:
        # 1. Close > 200-day SMA
        # 2. Cumulative RSI (sum of last 2 days' 3-period RSI) < 45
        if (self.data.Close[-1] > self.sma_200[-1]) and (self.cumulative_rsi_2[-1] < 45):
            if not self.position:
                self.buy()

        # Exit Condition:
        # 2-period RSI > 65
        if self.position:
            if self.rsi_2[-1] > 65:
                self.position.close()