from backtesting import Backtest, Strategy
from backtesting import set_bokeh_output
import pandas as pd

set_bokeh_output(notebook=False)

class BacktestEngine:
    def __init__(self, data, benchmark, strategy, cash=10000, commission=0.000, lookback=200):
        """
        Initializes the BacktestEngine.

        :param data: Pandas DataFrame with a DatetimeIndex.
        :param benchmark: Benchmark for comparison (not used in current implementation).
        :param strategy: Strategy class to be used for backtesting.
        :param cash: Initial cash for backtesting.
        :param commission: Commission fee per trade.
        :param lookback: Number of data points required for indicators (e.g., 200 for SMA200).
        """
        self.data = data.sort_index()  # Ensure data is sorted by date
        self.benchmark = benchmark
        self.strategy = strategy
        self.cash = cash
        self.commission = commission
        self.lookback = lookback  # Lookback in data points

    def run(self, window_size=2, step_size=6, plot=False):
        if not isinstance(self.data.index, pd.DatetimeIndex):
            self.data.index = pd.to_datetime(self.data.index)
        
        results_list = []

        start_date = self.data.index.min()
        end_date = self.data.index.max()

        # Convert window_size and step_size to frequency if needed
        # Assuming window_size is in years and step_size in months
        # This can be adjusted based on actual data frequency

        # Initialize the starting point
        current_train_end = start_date + pd.DateOffset(years=window_size)
        window_count = 0

        while current_train_end + pd.DateOffset(months=step_size) <= end_date:
            test_end = current_train_end + pd.DateOffset(months=step_size)

            # Define training data up to current_train_end
            train_data = self.data.loc[:current_train_end]

            # Define testing data
            test_data = self.data.loc[current_train_end:test_end]

            # Ensure that test_data has at least 'lookback' data points from train_data
            # Retrieve the last 'lookback' data points from train_data
            if len(train_data) < self.lookback:
                raise ValueError(f"Training data from {start_date} to {current_train_end} has fewer than {self.lookback} data points.")

            # Get the last 'lookback' data points for the test_data's initial data
            lookback_data = train_data.tail(self.lookback)
            combined_test_data = pd.concat([lookback_data, test_data])

            print(f"Window {window_count}:")
            print(f"  Training up to {current_train_end.date()}")
            print(f"  Testing from {current_train_end.date()} to {test_end.date()} with {self.lookback} lookback data points.")

            # Running the backtest on the training data.
            bt_train = Backtest(
                train_data,
                self.strategy,
                cash=self.cash,
                commission=self.commission,
                exclusive_orders=True  # Prevent overlap of trades
            )
            train_results = bt_train.run()

            # Running the backtest on the testing data with lookback
            bt_test = Backtest(
                combined_test_data,
                self.strategy,
                cash=self.cash,
                commission=self.commission,
                exclusive_orders=True
            )
            test_results = bt_test.run()

            if plot:
                # Optionally, plot each test segment. Comment out if plotting every segment is undesired.
                bt_test.plot()

            # Store the results along with the period info.
            results_list.append({
                'window': window_count,
                'train_period': (start_date, current_train_end),
                'test_period': (current_train_end, test_end),
                'train_results': train_results,
                'test_results': test_results
            })

            # Move the window forward
            current_train_end += pd.DateOffset(months=step_size)
            window_count += 1

        return results_list
