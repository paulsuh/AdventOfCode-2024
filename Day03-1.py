from re import findall

from Inputs.Day03_input import problem_input

# problem_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


match_list = findall(r"mul\((\d+),(\d+)\)", problem_input)

result = sum([
    int(x) * int(y)
    for x, y in match_list
])

print(result)
