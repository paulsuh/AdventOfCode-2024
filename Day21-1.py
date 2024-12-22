from pprint import pprint
from itertools import pairwise, permutations, product
from functools import cache
from enum import Enum

from Inputs.Day21_input import problem_input


problem_input = """029A
980A
179A
456A
379A"""

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
def base_routes_for_keypad(start: str, end: str, keypad_type: KeypadType) -> list[str]:
    # if moving down and right, move right first then down
    # if moving down and left, doesn't matter
    # if moving up and left, move up first then left
    # if moving up and right, doesn't matter
    if keypad_type == KeypadType.numeric:
        keypad = numeric_keypad
    else:
        keypad = directional_keypad
    start_coords = keypad[start]
    end_coords = keypad[end]
    row_delta = end_coords[0] - start_coords[0]
    col_delta = end_coords[1] - start_coords[1]
    base_moves = ("^" if row_delta < 0 else "v") * abs(row_delta) + \
                 ("<" if col_delta < 0 else ">") * abs(col_delta)
    all_moves = set(permutations(base_moves))

    return ["".join(one_route) + "A" for one_route in all_moves]


@cache
def pruned_routes_for_keypad(start: str, end: str, keypad_type: KeypadType) -> list[str]:
    all_direct_routes = base_routes_for_keypad(start, end, keypad_type)
    blocked_routes = base_routes_for_keypad(start, "b", keypad_type)
    if len(blocked_routes) > 0:
        prefix_len = len(blocked_routes[0])
        result = [
            one_route
            for one_route in all_direct_routes
            if one_route[:prefix_len] not in blocked_routes
        ]
        return result
    else:
        return all_direct_routes


def all_expansions_for_sequence(key_sequence: str, keypad_type: KeypadType) -> list[tuple[str, int]]:
    route_lists = []
    for start_key, end_key in pairwise("A" + key_sequence):
        key_pair_routes = pruned_routes_for_keypad(start_key, end_key, keypad_type)
        route_lists.append(key_pair_routes)
    all_alternative_routes = product(*route_lists)
    result = [
        (route_str := "".join(one_route), len(route_str))
        for one_route in all_alternative_routes
    ]
    return result


def min_length_expansions_for_sequence(key_sequence: str, keypad_type: KeypadType) -> list[tuple[str, int]]:
    all_expansions = all_expansions_for_sequence(key_sequence, keypad_type)
    min_len = min(x[1] for x in all_expansions)
    return [
        x
        for x in all_expansions
        if x[1] == min_len
    ]


def complete_expansion(numeric_key_sequence: str) -> list[tuple[str, int]]:
    numeric_expansion = min_length_expansions_for_sequence(numeric_key_sequence, KeypadType.numeric)
    first_directional_expansion = []
    for one_directional_ks in numeric_expansion:
        first_directional_expansion += min_length_expansions_for_sequence(one_directional_ks[0], KeypadType.directional)
    second_directional_expansion = []
    for one_more_directional_ks in first_directional_expansion:
        second_directional_expansion += min_length_expansions_for_sequence(one_more_directional_ks[0], KeypadType.directional)

    return second_directional_expansion


def complexity_calc(key_sequence: str) -> int:
    key_seq_expansion = complete_expansion(key_sequence)
    expansion_len = len(key_seq_expansion)
    numeric_part = int(key_sequence[:-1])
    print(key_sequence, expansion_len, numeric_part)
    return expansion_len * numeric_part


# x = min_length_expansions_for_sequence("029A", KeypadType.numeric)
# pprint(list(x))

complexity_total = 0
for one_numeric_sequence in sequence_list:
    complexity_total += complexity_calc(one_numeric_sequence)
print(complexity_total)
print(base_routes_for_keypad.cache_info())
print(pruned_routes_for_keypad.cache_info())
