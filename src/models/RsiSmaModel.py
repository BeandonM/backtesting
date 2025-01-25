from backtesting import Strategy
import pandas as pd

import talib

class RsiSmaModel(Strategy):

    def init(self):
        
        self.ma200 = self.I(talib.SMA, self.data.Close, timeperiod = 200)
        
        self.rsi2 = self.I(talib.RSI, self.data.Close,timeperiod=2)
        
        self.ma5 = self.I(talib.SMA, self.data.Close, timeperiod=5)

    def next(self):
        
        if self.position:
            if self.data.Close[-1] > self.ma5[-1]:
                self.position.close()
        else:
            if (self.data.Close[-1] > self.ma200[-1] and (self.rsi2[-1] < 9)):
                self.buy()