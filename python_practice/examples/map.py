def convert_to_int(value: str):
    return int(value)

b = list(map(convert_to_int, input().rstrip().split()))

print(b)