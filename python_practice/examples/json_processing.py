import json
import pandas as pd
from pathlib import Path
from collections import Counter

file_path = 'python_practice/examples' / Path('trade_history.json')
with open(file_path, 'r') as f:
    trades = json.load(f)

# some json processing
print(f"Number of trades per symbol {Counter(x['symbol'] for x in trades)}")

# get unique symbols
symbols = list(set(trade['symbol'] for trade in trades))

# highest price trade per symbol
max(trades, key=lambda x: x['price'])
