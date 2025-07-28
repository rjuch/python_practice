import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

# Pricing functions
def bs_price(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return np.exp(-q * T) * S * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
    return np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * S * norm.cdf(-d1)

def bs_greeks(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf = norm.pdf(d1)
    if option_type == 'call':
        delta = np.exp(-q * T) * norm.cdf(d1)
        theta = (-S * sigma * np.exp(-q * T) * pdf / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)
                 + q * S * np.exp(-q * T) * norm.cdf(d1))
    else:
        delta = -np.exp(-q * T) * norm.cdf(-d1)
        
        theta = (-S * sigma * np.exp(-q * T) * pdf / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)
                 - q * S * np.exp(-q * T) * norm.cdf(-d1))
    gamma = np.exp(-q * T) * pdf / (S * sigma * np.sqrt(T))
    vega = S * np.exp(-q * T) * pdf * np.sqrt(T)
    rho = (1 if option_type=='call' else -1) * K * T * np.exp(-r * T) * norm.cdf(d2 if option_type=='call' else -d2)
    return {
        'Delta': delta, 
        'Gamma': gamma, 
        'Vega': vega, 
        'Theta': theta, 
        'Rho': rho,
        'Premium': bs_price(S, K, T, r, q, sigma, option_type)
    }

def mc_digital(S, K, T, r, q, sigma, option_type, n_paths=100000, seed=None):
    if seed:
        np.random.seed(seed)
    Z = np.random.randn(n_paths)
    ST = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    pay = (ST > K).astype(float) if option_type=='call' else (ST < K).astype(float)
    return np.exp(-r * T) * pay.mean()

def mc_digital_greeks(S, K, T, r, q, sigma, option_type,
                   eps_S=1e-2, eps_sig=1e-4, eps_r=1e-4, eps_T=1e-3, n_paths=5_000_000, seed=42):
    # baseline
    V0 = mc_digital(S, K, T, r, q, sigma, option_type, n_paths, seed)

    # Delta & Gamma
    V_plus  = mc_digital(S+eps_S, K, T, r, q, sigma, option_type, n_paths, seed)
    V_minus = mc_digital(S-eps_S, K, T, r, q, sigma, option_type, n_paths, seed)
    delta = (V_plus - V_minus)/(2*eps_S)
    gamma = (V_plus - 2*V0 + V_minus)/(eps_S**2)

    # Vega
    V_sig_p = mc_digital(S, K, T, r, q, sigma+eps_sig, option_type, n_paths, seed)
    V_sig_m = mc_digital(S, K, T, r, q, sigma-eps_sig, option_type, n_paths, seed)
    vega = (V_sig_p - V_sig_m)/(2*eps_sig)

    # Rho
    V_r_p = mc_digital(S, K, T, r+eps_r, q, sigma, option_type, n_paths, seed)
    V_r_m = mc_digital(S, K, T, r-eps_r, q, sigma, option_type, n_paths, seed)
    rho   = (V_r_p - V_r_m)/(2*eps_r)

    # Theta (note the minus: price decreases as T decreases)
    V_T_p = mc_digital(S, K, T+eps_T, r, q, sigma, option_type, n_paths, seed)
    V_T_m = mc_digital(S, K, T-eps_T, r, q, sigma, option_type, n_paths, seed)
    theta = - (V_T_p - V_T_m)/(2*eps_T)

    return {
        'Delta': delta, 
        'Gamma': gamma, 
        'Vega': vega, 
        'Theta': theta, 
        'Rho': rho,
        'Premium': V0
    }

def worker(args):
    S, K, T, r, q, sigma, option_type = args
    return mc_digital_greeks(S, K, T, r, q, sigma, option_type)

if __name__ == '__main__':
    spot = 100
    strike = 100
    years_to_maturity = 1
    rf_rate = 0.05
    q = 0
    sigma = 0.20
    option_type = 'call'
    
    # option_model = 'vanilla'

    # # models_greeks = {
    # #     'vanilla': lambda s, strike, T, rf_rate, q, sigma, option_type, seed:
    # # }


    # print(bs_price(spot, strike, years_to_maturity, rf_rate, q, sigma, option_type))
    # print(bs_greeks(spot, strike, years_to_maturity, rf_rate, q, sigma, option_type))

    # d1 and d2 plotted
    # d1s = []
    # d2s = []
    # x = range(50, 201)
    # for S in x:
    #     d1 = (np.log(S / strike) + (rf_rate - q + 0.5 * sigma**2) * years_to_maturity) / (sigma * np.sqrt(years_to_maturity))
    #     d2 = d1 - sigma * np.sqrt(years_to_maturity)
    #     d1s.append(d1)
    #     d2s.append(d2)
    # pass

    # plt.plot(x, d1s, label='d1')
    # plt.plot(x, d2s, label='d2')
    # plt.plot(x, [d_1 - d_2 for d_1, d_2 in zip(d1s, d2s)], label='d1 - d2')
    # plt.title('plotting d1 and d2 from BS')
    # plt.xlabel('Spot')
    # plt.ylabel('Value')
    # plt.legend()
    # plt.show()

    # def plot_dict(x:list, y: dict, title:str, x_label:str, y_label:str):
    #     plt.figure()

    #     for key, val in y.items():
    #         plt.plot(x, val, label=f'{key}')
        
    #     plt.title(title)
    #     plt.xlabel(x_label)
    #     plt.ylabel(y_label)
    #     plt.legend()
    #     plt.show()


    # # Delta Vanilla Call
    # spot_range = range(75, 126)
    # deltas = {
    #     T: [
    #           bs_greeks(s, strike, T, rf_rate, q, sigma, 'call')['Delta'] 
    #           for s in spot_range
    #     ] 
    #     for T in [0.1, 0.25, 0.5, 1]
    # }

    # plot_dict(spot_range, deltas, 'Vanilla Call Delta', 'Spot', 'Delta')

    # # Gamma Vanilla Call
    # spot_range = range(75, 126)
    # deltas = {
    #     T: [
    #           bs_greeks(s, strike, T, rf_rate, q, sigma, 'call')['Gamma'] 
    #           for s in spot_range
    #     ] 
    #     for T in [0.1, 0.25, 0.5, 1]
    # }

    # plot_dict(spot_range, deltas, 'Vanilla Call Gamma', 'Spot', 'Gamma')

    spot_range = list(np.linspace(80, 120))#range(75, 126)
    # spot_range = [80, 90, 100, 110, 120]
    # spot_range = range(90, 120, 2)
    T_range = [0, 0.05, 0.25, 0.5, 1]
    greek_list = ['Premium', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
    greek_values = []
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(12, 8), sharex=True, sharey=False)
    # Flatten the axes array so we can iterate
    axes = axes.flatten()
    n_procs = min(cpu_count(), len(spot_range))

    for row_offset, option_type in enumerate(['call', 'put']): #
        for T in T_range:
            # Build argument tuples for this slice
            tasks = [
                (S, strike, T, rf_rate, q, sigma, option_type)
                for S in spot_range
            ]   

            # # Parallel map
            # with Pool(processes=n_procs) as pool:
            #     greek_values = pool.map(worker, tasks)

            greek_values = [bs_greeks(s, strike, T, rf_rate, q, sigma, option_type) for s in spot_range]
            # greek_values = [mc_digital_greeks(s, strike, T, rf_rate, q, sigma, option_type) for s in spot_range]
            for idx, greek in enumerate(greek_list):
                ax = axes[(row_offset * 6) + idx]
            
                ax.plot(spot_range, [x[greek] for x in greek_values], label=f'T={T:.2f} yr')
                ax.set_title(f'{option_type.capitalize()} - {greek}')
                # ax.set_xlabel('Spot Price')
                # ax.set_ylabel(greek)
                # ax.legend(fontsize=6)
                ax.xaxis.label.set_visible(False)
                ax.yaxis.label.set_visible(False)
                ax.set_facecolor('#f7f7f7')

                # Shared axis labels
                fig.supxlabel('Spot Price (S)', fontsize='medium', y=0.03)
                fig.supylabel('Greek Value', fontsize='medium')

                ax.grid(True) 

    handles, labels = axes[0].get_legend_handles_labels()

    # Place a single legend at the bottom
    fig.legend(
        handles, labels,
        loc='lower center',
        ncol=len(T_range),
        frameon=False,
        fontsize='small',
        bbox_to_anchor=(0.5, -0.01)
    )

    # Make room for the legend
    plt.tight_layout()

    # plt.subplots_adjust(bottom=0.15)

    mngr = plt.get_current_fig_manager()

    # Try backend‑specific maximize methods:
    try:
        # For Qt backends (Qt5Agg, etc.)
        mngr.window.showMaximized()
    except AttributeError:
        try:
            # For TkAgg
            mngr.window.state('zoomed')
        except Exception:
            # As a fallback, toggle full screen
            mngr.full_screen_toggle()

    plt.show()

    #     plt.figure()

    #     for key, val in y.items():
    #         plt.plot(x, val, label=f'{key}')
        
    #     plt.title(title)
    #     plt.xlabel(x_label)
    #     plt.ylabel(y_label)
    #     plt.legend()
    #     plt.show()

    pass

