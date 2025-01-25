from data.yFinanceData import get_ticker_data
from features.BacktestEngine import BacktestEngine
from models.DemoModel import Alpha3

data = get_ticker_data("SPY",start="2020-01-01", end="2025-01-01")
bt = BacktestEngine(data,None,Alpha3,10000,0.002)
results = bt.run(plot=True)
for period in results:
    print()
    print("TRAIN PERIOD:", period['train_period'])
    print(period['train_results'])
    print()
    print("TEST PERIOD:", period['test_period'])
    print(period['test_results'])
    print("=" * 80)
    print()