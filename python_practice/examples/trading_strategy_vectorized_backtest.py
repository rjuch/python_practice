import pandas as pd
from pathlib import Path

file_path = 'python_practice/examples' / Path('daily_candles.csv')
df_prices = pd.read_csv(file_path)

df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'])
df_prices.set_index('timestamp', inplace=True)

df_prices_matrix = df_prices.pivot(columns='symbol', values='C')

print(df_prices_matrix.head())

df_returns = df_prices_matrix / df_prices_matrix.shift(1) - 1
df_returns = df_returns.dropna()
print(df_returns.head())


pass
