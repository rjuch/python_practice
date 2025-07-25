'''
    # Euler-Maruyama formula
    S_EM[i+1] = S_EM[i] * (1 + r * dt + sigma * sqrt(dt) * w)

    # Milstein-scheme formula
    S_MIL[i+1] = S_MIL[i] * (1 + r * dt + sigma * sqrt(dt) * w + 0.5 * sigma**2 * (w**2 - 1) * dt)

    # Closed-form solution formula / Exact
    S_CF[i+1] = S_CF[i] * np.exp( (r - 0.5 * sigma**2) * dt + sigma * w * sqrt(dt))
'''

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time

def generate_gbm_price_series(start_price, mu, sigma, horizon, time_steps, num_sims, seed=None):
    np.random.seed(seed)
    dt = horizon / time_steps
    sims = np.zeros((int(time_steps), num_sims))

    sims[0] = start_price
    for i in range(int(time_steps)-1):
        w = np.random.standard_normal(num_sims)
        sims[i+1] = sims[i] * (1 + mu * dt + np.sqrt(dt) * sigma * w)
        pass
    return(sims)

def generate_gbm_price_series_no_loop(start_price, mu, sigma, horizon, time_steps, num_sims, seed=None):
    np.random.seed(seed)
    dt = horizon / time_steps
    sims = np.random.randn(int(time_steps), num_sims)
    

    sims = (1 + mu * dt + np.sqrt(dt) * sigma * sims)
    sims[0] = 1

    # sims[0] = start_price
    # for i in range(int(time_steps)-1):
    #     w = np.random.standard_normal(num_sims)
    #     sims[i+1] = sims[i] * (1 + mu * dt + np.sqrt(dt) * sigma * w)
    #     pass
    return np.cumprod(sims, axis=0) * start_price

def generate_random_trades_series(start_price, start_date, end_date, mu, sigma, num_sims=None, seed=None):
    # np.random.seed(seed)
    dates_days = [start_date + timedelta(days=1*x) for x in range((end_date - start_date).days)]
    pass


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    start_price = 100
    mu = 0.045
    sigma = 0.16
    horizon_years = 2
    time_steps = 252 * horizon_years
    sims = 5000

    start_time = time.time()
    simulations = generate_gbm_price_series(start_price, mu, sigma, horizon_years, time_steps, sims, seed=42)
    # simulations
    print(f'{time.time() - start_time}')
    print(simulations[-1])

    start_time = time.time()
    simulations2 = generate_gbm_price_series_no_loop(start_price, mu, sigma, horizon_years, time_steps, sims, seed=42)

    print(f'{time.time() - start_time}')
    print(simulations2[-1])

    # plt.plot(simulations)
    # plt.show()

    # start_date = datetime.strptime('2025-01-01 09:00:00', '%Y-%m-%d %H:%M:%S')
    # end_date = datetime.strptime('2025-01-31 17:00:00', '%Y-%m-%d %H:%M:%S')

    # trades = generate_random_trades_series(start_price, start_date, end_date, mu, sigma)


