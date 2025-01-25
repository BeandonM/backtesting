from backtesting import Strategy
import pandas as pd

import talib

class Alpha3(Strategy):

    def init(self):

        # Create a pandas Series for open and volume from the data
        self.open_series = pd.Series(self.data.Open)
        self.volume_series = pd.Series(self.data.Volume)

        # Compute rank values for open and volume
        # Using self.I to ensure these are calculated only once.
        self.open_rank = self.I(lambda: self.open_series.rank(), name='open_rank')
        self.volume_rank = self.I(lambda: self.volume_series.rank(), name='volume_rank')

    def next(self):
      if len(self.open_rank) < 10:
        return
      # Calculate rolling correlation between the ranked open and volume series using the last 10 bars
      open_window = pd.Series(self.open_rank[-10:])
      volume_window = pd.Series(self.volume_rank[-10:])
      raw_corr = open_window.corr(volume_window)

      signal = -1 * raw_corr

      # Define a threshold
      threshold = 0.5

      # Implement the trading logic using the inverted correlation (signal):
      if signal > threshold:
          # Enter long only if you aren't already in one.
          if not self.position:
              self.buy()
      else:
          # Otherwise, if you are in a long position, exit (remain flat).
          if self.position:
              self.position.close()