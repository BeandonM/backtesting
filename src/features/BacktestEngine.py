from backtesting import Backtest, Strategy
import pandas as pd
class BacktestEngine:
    def __init__(self, data, strategy, cash=10000, comission = 0.00):
        self.data = data
        self.strategy = strategy
        self.cash = cash
        self.comission = comission