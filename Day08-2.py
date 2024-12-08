from itertools import product, combinations
from pprint import pprint
from operator import add

from Inputs.Day08_input import problem_input

# problem_input = """............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............"""


max_row = -1
max_col = -1

def calc_antenna_coords(map: str) -> dict:
    global max_row
    global max_col

    result = {}
    for row, one_line in enumerate(map.splitlines()):
        for col, one_char in enumerate(one_line):
            if one_char != ".":
                result.setdefault(one_char, []).append((row, col))
    max_row = row + 1
    max_col = col + 1
    return result


def calc_antinodes_for_one_antenna_type(antennas: list[tuple[int, int]]) -> set[tuple[int, int]]:
    result = set()
    for a1, a2 in combinations(antennas, 2):
        delta_y = a1[0] - a2[0]
        delta_x = a1[1] - a2[1]
        current_an = a1
        while 0 <= current_an[0] < max_row and 0 <= current_an[1] < max_col:
            result.add(current_an)
            current_an = tuple(map(add, current_an, (delta_y, delta_x)))
        current_an = a1
        while 0 <= current_an[0] < max_row and 0 <= current_an[1] < max_col:
            result.add(current_an)
            current_an = tuple(map(add, current_an, (-delta_y, -delta_x)))
    return result


def calc_antinodes(antennas_dict: dict[str, list[tuple[int, int]]]) -> set[tuple[int, int]]:
    result = set()
    for a_list in antennas_dict.values():
        a_nodes = calc_antinodes_for_one_antenna_type(a_list)
        result |= a_nodes
    return result


antennas = calc_antenna_coords(problem_input)
pprint(antennas)
print(max_row, max_col)
anti_nodes = calc_antinodes(antennas)
pprint(anti_nodes)
print(len(anti_nodes))
