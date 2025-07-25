import numpy as np
from scipy.stats import norm

# np.random.seed(42)

# # generate array of uniform random numbers
# x_uni = np.random.rand(5)
# print('\nUniform RV using rand:')
# print(x_uni)

# # generate array of normal random numbers
# print('\nStandard normal RV using standard_norm')
# print(np.random.standard_normal(5))

# # convert uniform random numbers to std normal
# print('\nStandard normal RV from uniform')
# print(norm.ppf(x_uni)) 
# pass

# matrix operations
A = np.array([[1,2], [2,5]])
x = np.array([[2], [3]])
B = np.dot(A, x)
# A . B
print('A:')
print(A)
print('x:')
print(x)
print('B:')
print(B)
print('A inverse')
print(np.linalg.inv(A))
print('A_inv.B')
print(np.dot(np.linalg.inv(A), B))
print('Det A', np.linalg.det(A))
m = 4
n = 4
print(np.zeros((m, n)))
print(np.ones((m, n)))
print(np.eye(n))
print(np.full((m, n), 3))
print(np.random.rand(m, n))

# eigen values
C = np.array([[1,0], [0,1]])
print(np.linalg.eig(C))

C = np.array([[0,0], [0,0]])
print(np.linalg.eig(C))
pass


np.cumprod(arr, axis=0)

slicing