from pprint import pprint
from operator import add
from typing import NamedTuple

from Inputs.Day20_input import problem_input


# problem_input = """###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############"""


# Pythonic cheat for out of bounds
race_map = [
    one_line + "#"
    for one_line in problem_input.splitlines()
]
race_map.append("#" * len(race_map[0]))

# pprint(race_map)

class Location(NamedTuple):
    row: int
    col: int

    def move(self, move_dirs: tuple[int, int]) -> "Location":
        return Location(self.row + move_dirs[0], self.col + move_dirs[1])


def locate_letter(letter: str) -> Location:
    for row, row_string in enumerate(race_map):
        if (col := row_string.find(letter)) > 0:
            return Location(row, col)


race_start = locate_letter("S")
race_end = locate_letter("E")

move_directions = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
)

race_path = [race_start]
while race_path[-1] != race_end:
    for one_move in move_directions:
        possible_next_move = race_path[-1].move(one_move)
        if possible_next_move in race_path:
            # backtrack
            continue
        if race_map[possible_next_move.row][possible_next_move.col] in ".E":
            race_path.append(possible_next_move)
            break

race_base_length = len(race_path)

# pprint(race_path)
print(race_base_length)

cheat_directions = (
    ((1, 0), (2, 0)),
    ((-1, 0), (-2, 0)),
    ((0, 1), (0, 2)),
    ((0, -1), (0, -2))
)


def hamming_distance(loc1: Location, loc2: Location) -> int:
    return abs(loc1.row - loc2.row) + abs(loc1.col - loc2.col)


def find_cheats_for_location(loc: Location, remaining_locs: list[Location]) -> int:
    result = 0
    for one_dest in remaining_locs:
        if (cheat_steps := hamming_distance(loc, one_dest)) <= 20:
            if (dist_saved := race_path.index(one_dest) - race_path.index(loc) - cheat_steps) >= 100:
                result += 1

    return result


total_cheats = 0
for loc_index, one_loc in enumerate(race_path):
    if loc_index % 100 == 0:
        print(".", end="")
    if loc_index % 1000 == 0:
        print()
    total_cheats += find_cheats_for_location(one_loc, race_path[loc_index+1:])

# pprint(all_cheats)
print(total_cheats)

# all_vals = list(set(all_cheats.values()))
# all_vals.sort()
# for t in all_vals:
#     print(list(all_cheats.values()).count(t), t)
