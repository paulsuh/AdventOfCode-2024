from Inputs.Day01_input import col1, col2


col1.sort()
col2.sort()

result = sum([
    abs(c1 - c2)
    for c1, c2 in zip(col1, col2)
])

print(result)
