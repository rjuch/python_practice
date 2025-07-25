my_float = 0.1 + 0.2
print(my_float)


import math
math.isclose(my_float, 0.3)


from decimal import Decimal, getcontext

getcontext().prec = 10  # Set precision to 10 decimal places
x = Decimal('1') / Decimal('7')
print(x)  # → 0.1428571429

float_better = Decimal('0.1') + Decimal('0.2')
print(float_better)
pass