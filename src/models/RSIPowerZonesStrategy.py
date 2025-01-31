import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class RSIPowerZonesStrategy(Strategy):
    # Strategy parameters
    SMA_PERIOD = 200
    RSI_PERIOD = 4
    RSI_ENTRY_THRESHOLD = 30
    RSI_DOUBLE_THRESHOLD = 25
    RSI_EXIT_THRESHOLD = 55

    def init(self):
        # Calculate indicators
        self.sma_200 = self.I(talib.SMA, self.data.Close, timeperiod=self.SMA_PERIOD)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.RSI_PERIOD)
        self.double_position = False  # Flag to track if we've doubled

    def next(self):
        # Ensure indicators have valid values
        if self.sma_200[-1] is None or self.rsi[-1] is None:
            return

        # **Entry Condition:**
        if (self.data.Close[-1] > self.sma_200[-1]) and (self.rsi[-1] < self.RSI_ENTRY_THRESHOLD):
            # Buy only if no positions are open
            if not self.position:
                self.buy()
                self.double_position = False  # Reset doubling flag

        # **Position Doubling:**
        if self.position and not self.double_position and (self.rsi[-1] < self.RSI_DOUBLE_THRESHOLD):
            # Buy a second unit (double the position)
            self.buy()
            self.double_position = True  # Prevent multiple doublings

        # **Exit Condition:**
        if self.position and (self.rsi[-1] > self.RSI_EXIT_THRESHOLD):
            self.position.close()
            self.double_position = False  # Reset doubling flag after exiting