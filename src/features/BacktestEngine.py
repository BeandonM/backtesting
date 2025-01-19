from backtesting import Backtest, Strategy
import pandas as pd
class BacktestEngine:
    def __init__(self, data, benchmark, strategy, cash=10000, comission = 0.00):
        self.data = data
        self.benchmark = benchmark
        self.strategy = strategy
        self.cash = cash
        self.comission = comission
        
    def run(self, window_size = 2, step_size = 6, plot = False):
        if not isinstance(self.data.index, pd.DatetimeIndex):
            self.data.index = pd.to_datetime(self.data.index)
        results_list = []

        start_date = self.data.index.min()
        end_date = self.data.index.max()

        current_train_start = start_date

        train_offset = pd.DateOffset(years=window_size)
        test_offset = pd.DateOffset(months=step_size)

        window_count = 0

        while True:
            train_end = current_train_start + train_offset
            test_end = train_end + test_offset

            if test_end > end_date:
                break

            print(f"Window {window_count}: Training from {current_train_start.date()} to {train_end.date()}, "
                    f"Testing from {train_end.date()} to {test_end.date()}")
            train_data = self.data.loc[current_train_start:train_end]
            test_data = self.data.loc[train_end:test_end]

            # Running the backtest on the training data.
            bt_train = Backtest(train_data, self.strategy, cash=self.cash, commission=self.commission)
            train_results = bt_train.run()

            # Running the backtest on the testing data.
            bt_test = Backtest(test_data, self.strategy, cash=self.cash, commission=self.commission)
            test_results = bt_test.run()

            if plot:
                # Optionally, plot each test segment. Comment out if plotting every segment is undesired.
                bt_test.plot()

            # Store the results along with the period info.
            results_list.append({
                'train_period': (current_train_start, train_end),
                'test_period':  (train_end, test_end),
                'train_results': train_results,
                'test_results':  test_results
            })
            
            current_train_start = current_train_start + test_offset
            window_count += 1
        return results_list