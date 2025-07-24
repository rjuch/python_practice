import numpy as np
import random
from decorators import timeit_decorator

arr = [[11, 2, 4], [4, 5, 6], [10, 8, -12]]
# arr_dim = 10000
#arr = [[int(random.random()*100) for _ in range(arr_dim)] for _ in range(arr_dim)]
# arr = np.random.randint(0, 100, size=(arr_dim, arr_dim))
print('done genrating grid')

@timeit_decorator
def diag_abs_diff_method1():
    arr_size = len(arr)

    primary_diag = []
    secondary_diag = []

    for r in range(arr_size):
        for c in range(arr_size):
            if r == c:
                # main diagonal
                # print('primary:', arr[r][c])
                primary_diag.append(arr[r][c])
            
            if r+c == arr_size - 1:
                # secondary diagonal
                # print('secondary:', arr[r][c])
                secondary_diag.append(arr[r][c])
    print('primary:', primary_diag)
    print('secondary:', secondary_diag)

@timeit_decorator
def diag_abs_diff_method2():
    arr_size = len(arr)

    primary_diag = []
    secondary_diag = []

    for r in range(arr_size):
        primary_diag.append(arr[r][r])

    for r in range(arr_size):
        secondary_diag.append(arr[r][arr_size-1-r])

    print('primary:', primary_diag)
    print('secondary:', secondary_diag)

diag_abs_diff_method1()
diag_abs_diff_method2()

