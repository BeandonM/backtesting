from data.yFinanceData import get_ticker_data
from features.BacktestEngine import BacktestEngine
from models.RsiSmaModel import RsiSmaModel

data = get_ticker_data("SPY",start="2019-01-01", end="2025-01-03")
bt = BacktestEngine(data,data,RsiSmaModel,10000,0.002)
results = bt.run(window_size=3,step_size=6,plot=False)
for period in results:
    print()
    print("TRAIN PERIOD:", period['train_period'])
    print(period['train_results'])
    print()
    print("TEST PERIOD:", period['test_period'])
    print(period['test_results'])
    print("=" * 80)
    print()
# Assuming 'results' is your list of backtest results
# and each 'period' is a dictionary with keys:
# 'train_period', 'train_results', 'test_period', 'test_results'

# Define the filename where you want to save the results
output_filename = 'backtest_results.txt'

# Open the file in write mode using a context manager
with open(output_filename, 'w') as f:
    for period in results:
        # Optional: Add a newline for better readability
        print("\n", file=f)
        
        # Print Training Period
        print("TRAIN PERIOD:", period['train_period'], file=f)
        print(period['train_results'], file=f)
        
        # Optional: Add another newline for spacing
        print("\n", file=f)
        
        # Print Testing Period
        print("TEST PERIOD:", period['test_period'], file=f)
        print(period['test_results'], file=f)
        
        # Separator for readability
        print("=" * 80, file=f)
        print("\n", file=f)

print(f"Backtest results have been written to {output_filename}")