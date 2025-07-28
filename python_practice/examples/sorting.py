# bubble sort, stable but slow. O(n) -> O(n^2)

def sort_bubble(values: list, ascending=True):
    n_count = 0  # jsut for checking how many times loop runs
    swapped_flag = True
    while swapped_flag:
        swapped_flag = False
        for i in range(len(values) - 1):
            if (values[i] > values[i+1] and ascending) or \
               (values[i] < values[i+1] and not ascending):
                temp_val = values[i]
                values[i] = values[i+1]
                values[i+1] = temp_val
                swapped_flag = True
                n_count += 1
    print('n =', n_count)
    return values


if __name__ == '__main__':
    arr = sorted([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1])
    print('Before:', arr)
    arr_sorted = sort_bubble(arr)
    print('After:', arr_sorted)

    arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1]
    print('Before:', arr)
    arr_sorted = sort_bubble(arr)
    print('After:', arr_sorted)

    arr = sorted([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1])
    print('Before:', arr)
    arr_sorted = sort_bubble(arr, ascending=False)
    print('After:', arr_sorted)
