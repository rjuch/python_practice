import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Black–Scholes gamma
def bs_gamma(S, K, T, r, q, sigma):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S*sigma*np.sqrt(T))

# Parameters
K     = 100
r     = 0.05
q     = 0.0
sigma = 0.2
S     = np.linspace(50, 150, 400)

# A list of maturities to compare
T_list = [0.25, 0.5, 1.0, 2.0]

# Create a 2×2 grid of subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8), sharex=True, sharey=True)

# Flatten the axes array so we can iterate
axes = axes.flatten()

for ax, T in zip(axes, T_list):
    gamma_vals = bs_gamma(S, K, T, r, q, sigma)
    ax.plot(S, gamma_vals, label=f'T={T:.2f} yr')
    ax.set_title(f'Gamma Profile (T={T:.2f})')
    ax.set_xlabel('Spot Price (S)')
    ax.set_ylabel('Gamma')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()
