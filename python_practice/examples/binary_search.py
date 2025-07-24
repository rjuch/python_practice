'''
Binary search returns position of value in an ordered list
'''
def binary_search(values: list, target: int):
    current_min = 0
    current_max = len(values) - 1
    # guess = int((current_max - current_min) / 2)

    while current_max >= current_min:
        guess = current_min + int((current_max - current_min) / 2)
        if values[guess] == target:
            return guess
        elif values[guess] > target:
            current_max = guess - 1
        else:
            current_min = guess + 1
        # if current_min + int((current_max - current_min) / 2) == guess:
        #     return None
        
    

value_list = [x for x in range(0,101,2)]
print(value_list)

target_val = 102
pos = binary_search(value_list, target_val)
if pos:
    print(f'target value: {target_val} found, position: {pos} actual value: {value_list[pos]}')
else:
    print(f'target value: {target_val} not found')
