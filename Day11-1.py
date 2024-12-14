from pprint import pprint
from functools import cache

from Inputs.Day11_input import problem_input


# problem_input = "0 1 10 99 999"

# problem_input = "125 17"


stones_list = [
    int(x)
    for x in problem_input.split()
]

pprint(stones_list)


@cache
def blink(stone: int, depth: int) -> list[int]:
    if depth == 0:
        return [stone]
    elif stone == 0:
        return blink(1, depth-1)
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        stone_len = len(stone_str) // 2
        return blink(int(stone_str[:stone_len]), depth-1) + \
            blink(int(stone_str[stone_len:]), depth-1)
    else:
        return blink(stone*2024, depth-1)


result = 0
for one_stone in stones_list:
    expansion = blink(one_stone, 25)
    result += len(expansion)

print(result)
