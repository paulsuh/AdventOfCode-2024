from Inputs.Day01_input import col1, col2


result = sum([
    sum([
        c2
        for c2 in col2
        if c2 == c1
    ])
    for c1 in col1
])

print(result)
