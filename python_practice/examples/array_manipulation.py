def arrayManipulation(n, queries):
    arr = [0] * (n + 2)  # Use n+2 to avoid boundary issues

    for a, b, k in queries:
        arr[a] += k
        arr[b + 1] -= k

    max_value = 0
    current = 0
    for i in range(1, n + 1):
        current += arr[i]
        if current > max_value:
            max_value = current

    return max_value


n = 5
queries = [
    [1, 2, 100],
    [2, 5, 100],
    [3, 4, 100]
]
print(arrayManipulation(n, queries))  # Output: 200