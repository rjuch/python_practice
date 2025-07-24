import json
import pandas as pd
from pathlib import Path

def generate_candles_from_trades(df_trades: pd.DataFrame):
    candles = (
        df_trades.groupby('symbol')
            .resample('D')
            .agg({
                'price': ['first', 'max', 'min', 'last'], 
                'volume': 'sum'
            })
            .reset_index()
    )
    candles.columns = ['symbol', 'timestamp', 'O', 'H', 'L', 'C', 'V']
    # candles.columns = ['_'.join(col).strip('_') for col in candles.columns.values]
    # candles.rename(columns={'price_first': 'O','price_max': 'H','price_min': 'L','price_last': 'C'})
    return candles
    
file_path = 'python_practice/examples' / Path('trade_history.json')
with open(file_path, 'r') as f:
    trades = json.load(f)

df_trades = pd.DataFrame(trades)
df_trades['timestamp'] = pd.to_datetime(df_trades['timestamp'])
df_trades.set_index('timestamp', inplace=True)

candles = generate_candles_from_trades(df_trades)

print(candles)

import matplotlib.pyplot as plt

for symbol in list(candles['symbol'].unique()):
    plt.plot(candles[candles['symbol'] == symbol].set_index('timestamp')['C'])
plt.show()

pass

