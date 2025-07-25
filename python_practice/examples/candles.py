import json
import pandas as pd
from pathlib import Path

def generate_candles_from_trades(df_trades: pd.DataFrame, period:str='D'):
    candles = (
        df_trades.groupby('symbol')
            .resample(period)
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

candles = generate_candles_from_trades(df_trades, '1d')
candles.set_index('timestamp', inplace=True)
print(candles)
#candles.to_csv('daily_candles.csv')

# import matplotlib.pyplot as plt

# for symbol in list(candles['symbol'].unique()):
#     plt.plot(candles[candles['symbol'] == symbol]['C'])
# plt.show()

# # normalised plots
# candles['C_norm'] = candles.groupby('symbol')['C'].transform(lambda x: x / x.iloc[0])
# for symbol in list(candles['symbol'].unique()):
#     plt.plot(candles[candles['symbol'] == symbol]['C_norm'])
# plt.show()
# pass


pass

symbol = 'AAPL'

import plotly.graph_objects as go

fig = go.Figure(data=go.Candlestick(
    x=candles[candles['symbol'] == symbol].index,
    open=candles[candles['symbol'] == symbol]['O'],
    high=candles[candles['symbol'] == symbol]['H'],
    low=candles[candles['symbol'] == symbol]['L'],
    close=candles[candles['symbol'] == symbol]['C']
))
fig.update_layout(title='OHLC Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
fig.show()
pass