from pprint import pprint
from itertools import pairwise, permutations, product
from functools import cache
from enum import Enum

from Inputs.Day21_input import problem_input


# problem_input = """029A
# 980A
# 179A
# 456A
# 379A"""

sequence_list = problem_input.splitlines()

numeric_keypad = {
    "b": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}
directional_keypad = {
    "b": (0, 0),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "^": (0, 1),
    "A": (0, 2)
}

class KeypadType(Enum):
    numeric = 1
    directional = 2


@cache
def possible_routes_for_keypad(start: str, end: str, keypad_type: KeypadType) -> set[str]:
    # if moving down and right, move right first then down
    # if moving down and left, move down then left
    # if moving up and right, move right first then up
    # if moving up and left, move up first then left
    if keypad_type == KeypadType.numeric:
        keypad = numeric_keypad
        blank_tile = (3, 0)
    else:
        keypad = directional_keypad
        blank_tile = (0, 0)
    start_coords = keypad[start]
    end_coords = keypad[end]
    row_delta = end_coords[0] - start_coords[0]
    col_delta = end_coords[1] - start_coords[1]
    r_move = "^" if row_delta < 0 else "v"
    c_move = "<" if col_delta < 0 else ">"

    result = set()
    if (start_coords[0], end_coords[1]) != blank_tile:
        result.add(abs(col_delta) * c_move + abs(row_delta) * r_move + "A")
    if (end_coords[0], start_coords[1]) != blank_tile:
        result.add(abs(row_delta) * r_move + abs(col_delta) * c_move + "A")
    return result


def expansions_for_sequence(key_sequence: str, keypad_type: KeypadType) -> set[str]:
    pairs_routes_list = []
    for start_key, end_key in pairwise("A" + key_sequence):
        key_pair_routes = possible_routes_for_keypad(start_key, end_key, keypad_type)
        pairs_routes_list.append(key_pair_routes)
    all_possible_routes = {
        "".join(one_route)
        for one_route in product(*pairs_routes_list)
    }
    # all_lens = {
    #     len(r)
    #     for r in all_possible_routes
    # }
    # print(all_lens)
    min_len = min([len(r) for r in all_possible_routes])
    result = {
        r
        for r in all_possible_routes
        if len(r) == min_len
    }
    return result


@cache
def shortest_expansions_for_stage(key_sequences: tuple[str]) -> tuple[str]:
    result = set()
    for one_sequence in key_sequences:
        expansion = expansions_for_sequence(one_sequence, KeypadType.directional)
        result |= expansion
    min_len = min(len(r) for r in result)
    result2 = (
        r
        for r in result
        if len(r) == min_len
    )
    return result2


def complete_expansion(numeric_key_sequence: str) -> int:
    prev_expansion = expansions_for_sequence(numeric_key_sequence, KeypadType.numeric)
    # print(numeric_expansion)
    for i in range(5):
        prev_expansion = shortest_expansions_for_stage(prev_expansion)
    # print(first_dir_expansion_result)
    min_len = len(prev_expansion.pop())
    print(min_len)
    return min_len


def complexity_calc(key_sequence: str) -> int:
    key_seq_len = complete_expansion(key_sequence)
    numeric_part = int(key_sequence[:-1])
    print(key_seq_len, numeric_part)
    return key_seq_len * numeric_part


# print(possible_routes_for_keypad("A", "7", KeypadType.numeric))
# print(possible_routes_for_keypad("A", "v", KeypadType.directional))
# print(expansions_for_sequence("379A", KeypadType.numeric))

# complete_expansion("379A")

complexity_total = 0
for one_numeric_sequence in sequence_list:
    complexity_total += complexity_calc(one_numeric_sequence)
print(complexity_total)

# print(base_routes_for_keypad.cache_info())
# print(pruned_routes_for_keypad.cache_info())


#   3  p  6  9 8   7 p    8  9 p  6   3 A p
# ('^  A  ^  ^ <   < A    >  > A  v   v v A ', 14)
# ('<A >A <A A v<A A >>^A vA A ^A v<A A A >^A', 28)
# ('v<<A^>>AvA^Av<<A^>>AAv<A<A^>>AA<Av>AA^Av<A^>AA<A>Av<A<A^>>AAA<Av>A^A', 68)
