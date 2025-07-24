import numpy as np
from scipy.stats import norm

np.random.seed(42)

# generate array of uniform random numbers
x_uni = np.random.rand(5)
print('\nUniform RV using rand:')
print(x_uni)

# generate array of normal random numbers
print('\nStandard normal RV using standard_norm')
print(np.random.standard_normal(5))

# convert uniform random numbers to std normal
print('\nStandard normal RV from uniform')
print(norm.ppf(x_uni)) 
pass
