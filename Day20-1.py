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
# print(race_base_length)

cheat_directions = (
    ((1, 0), (2, 0)),
    ((-1, 0), (-2, 0)),
    ((0, 1), (0, 2)),
    ((0, -1), (0, -2))
)


def find_cheats_for_location(loc: Location) -> dict[tuple[Location, Location, Location], int]:
    result = {}
    for cheat_move_one, cheat_move_two in cheat_directions:
        cheat_loc_one = loc.move(cheat_move_one)
        cheat_loc_two = loc.move(cheat_move_two)
        if race_map[cheat_loc_one.row][cheat_loc_one.col] == "#" and \
                race_map[cheat_loc_two.row][cheat_loc_two.col] in ".E":
            # check if the cheat moves forward or backwards
            if (picoseconds_saved := race_path.index(cheat_loc_two) - race_path.index(loc) - 2) > 0:
                result[(loc, cheat_loc_one, cheat_loc_two)] = picoseconds_saved

    return result


all_cheats = {}
for one_loc in race_path:
    all_cheats.update(find_cheats_for_location(one_loc))

pprint(all_cheats)
cheat_gt_100 = [
    x
    for x in all_cheats.values()
    if x >= 100
]
print(len(cheat_gt_100))

# all_vals = list(set(all_cheats.values()))
# all_vals.sort()
# for t in all_vals:
#     print(t, list(all_cheats.values()).count(t))
