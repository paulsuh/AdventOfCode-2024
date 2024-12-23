from pprint import pprint

from Inputs.Day22_input import problem_input


# problem_input = """1
# 10
# 100
# 2024"""

input_nums = [
    int(x)
    for x in problem_input.splitlines()
]

# pprint(input_nums)


def step1(x: int) -> int:
    x1 = x << 6
    result = (x ^ x1) & 16777215
    return result


def step2(x: int) -> int:
    x1 = x >> 5
    result = (x ^ x1) & 16777215
    return result


def step3(x: int) -> int:
    x1 = x << 11
    result = (x ^ x1) & 16777215
    return result


def all_steps(x: int) -> int:

    x1 = (x ^ (x << 6)) & 16777215
    x2 = (x1 ^ (x1 >> 5))
    x3 = (x2 ^ (x2 << 11)) & 16777215
    return x3


result = 0
for one_trader in input_nums:
    x = one_trader
    for i in range(2000):
        x = all_steps(x)
    print(one_trader, x)
    result += x

print(result)



# bit number                321098765432109876543210
# original                  111111111111111111111111
# shift left 6        111111111111111111111111000000
# xor                 111111000000000000000000111111
# trim                      000000000000000000111111
# shift right 5             000000000000000000000001
# xor                       000000000000000000111110
# trim                      000000000000000000111110
# shift left 11  00000000000000000011111000000000000
# xor            00000000000000000011111000000111110
# trim                      000000011111000000111110


# s1 = step1(123)
# print(s1)
# s2 = step2(s1)
# print(s2)
# s3 = step3(s2)
# print(s3)
# c1 = all_steps(123)
# print(c1)
#
# s1 = step1(s3)
# print(s1)
# s2 = step2(s1)
# print(s2)
# s3 = step3(s2)
# print(s3)
# c2 = all_steps(c1)
# print(c2)

