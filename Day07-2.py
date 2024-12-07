from functools import cache
from itertools import pairwise
from pprint import pprint
from operator import add, mul

from Inputs.Day07_input import problem_input



# problem_input = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20"""


problem_list = [
    one_line.split(": ")
    for one_line in problem_input.splitlines()
]

problem_list = [
    (int(one_list[0]), [int(x) for x in one_list[1].split()][::-1])
    for one_list in problem_list
]
pprint(problem_list)


def concat(x: int, y: int) -> int:
    return int(str(x) + str(y))


def dfs(operands: list[int]) -> list[int]:

    result = []
    operand1 = operands.pop()
    operand2 = operands.pop()
    for operator in (add, mul, concat):
        op_result = operator(operand1, operand2)
        if len(operands) == 0:
            result.append(op_result)
        else:
            updated_operands = operands.copy()
            updated_operands.append(op_result)
            result += dfs(updated_operands)
    return result


result = 0
for one_eq in problem_list:
    if one_eq[0] in dfs(one_eq[1]):
        result += one_eq[0]

print(result)
