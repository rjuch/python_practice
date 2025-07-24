'''
Function accepts a vector, interpolates missing values, backfills missing values at the start and forward fills missing values at the end
'''
import numpy as np

# vector interpolator
def linear_interpolate(x, x0, x1, y0, y1):
    # print(x, x0, x1, y0, y1)
    return y0 + (x - x0) * ((y1 - y0)/(x1 - x0))

def interpolate_vector(vector: list):
    ''' 
    Interpolates missing values: None
    if values missing at start, use first value
    if values missing at end, use last value
    '''
    output_vector = vector.copy()
    array_length = len(vector)
    # print(f'{vector} length {array_length}')

    for x in range(array_length):
        if output_vector[x] is None:
            x0 = None
            x1 = None
            
            # find previous non empty value
            for j in range(x, -1, -1):
                if output_vector[j]:
                    x0 = j
                    break

            # find next non empty value
            for j in range(x, array_length):
                if output_vector[j]:
                    x1 = j
                    break
            
            if x0 and x1:   # Interpolate
                interpolated_val = linear_interpolate(x, x0, x1, output_vector[x0], output_vector[x1])
                output_vector[x] = interpolated_val

            elif x0: # backfill values
                output_vector[x] = output_vector[x0]

            elif x1: # Forward fill
                output_vector[x] = output_vector[x1]
            
    return output_vector

values = [None, 1, 2, 3, None, 5, None, None, 7, None, None, None]
filled_values = interpolate_vector(values)
# print(values)
# print(filled_values)
import pandas as pd
print(pd.DataFrame([x for x in zip(values, filled_values)]))

# import matplotlib.pyplot as plt
# plt.plot([x for x in range(len(values))], filled_values)
# #plt.plot([x for x in range(len(values))], values)
# plt.show()