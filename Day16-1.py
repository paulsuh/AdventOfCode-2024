from collections import deque
from typing import NamedTuple
from pprint import pprint

from Inputs.Day16_input import problem_input


problem_input = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


# row, col, row_move, col_move
class Location(NamedTuple):
    row: int
    column: int
    row_move: int
    col_move: int


problem_map = [
    one_line
    for one_line in problem_input.splitlines()
]

start_row = len(problem_map) - 2
start_col = 1
start_row_move = 0
start_col_move = 1
start_location = Location(start_row, start_col, start_row_move, start_col_move)
end_row = 1
end_col = len(problem_map[0]) - 2

print(problem_map[start_row][start_col])
print(problem_map[end_row][end_col])

# (row, col, entry dir row, entry dir col): cost
costs_list: dict[Location, int] = {}

dir_cost_lookup = {
    # cur row move, cur col move, new row move, new col move
    # from down
    (1, 0, 1, 0): 0,
    (1, 0, 0, -1): 1000,
    (1, 0, -1, 0): 2000,
    (1, 0, 0, 1): 1000,
    # from up
    (-1, 0, -1, 0): 0,
    (-1, 0, 0, -1): 1000,
    (-1, 0, 1, 0): 2000,
    (-1, 0, 0, 1): 1000,
    # from left
    (0, -1, 0,-1): 0,
    (0, -1, 1, 0): 1000,
    (0, -1, -1, 0): 1000,
    (0, -1, 0, 1): 2000,
    # from right
    (0, 1, 0, 1): 0,
    (0, 1, 1, 0): 1000,
    (0, 1, -1, 0): 1000,
    (0, 1, 0, -1): 2000,
}


def get_next_locations(loc: Location) -> list[tuple[Location, Location]]:
    result = []
    for row_move, col_move in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if problem_map[loc.row + row_move][loc.column + col_move] in ".E":
            result.append((loc, Location(loc.row+row_move, loc.column+col_move, row_move, col_move)))
    return result


def get_location_cost(old_loc: Location,
                      new_loc: Location
                      ) -> int:    # cost, new Location
    old_loc_cost = costs_list[old_loc]
    rotation_cost = dir_cost_lookup[(old_loc.row_move, old_loc.col_move,
                                     new_loc.row_move, new_loc.col_move)]
    step_cost = 1
    result = old_loc_cost + rotation_cost + step_cost
    return result


# x = get_next_locations(start_location.row, start_location.column)
# for one_location in x:
#     c = get_location_cost(start_location, one_location)
#     print(one_location, c)


locations_to_be_checked: deque[tuple[Location, Location]] = deque()
locations_to_be_checked.extend(get_next_locations(start_location))
costs_list[start_location] = 0
# print(locations_to_be_checked)
while len(locations_to_be_checked) > 0:
    check_pair = locations_to_be_checked.popleft()
    current_loc = check_pair[0]
    check_loc = check_pair[1]
    new_cost = get_location_cost(current_loc, check_loc)
    if costs_list.setdefault(check_loc, 10000000000000) > new_cost:
        costs_list[check_loc] = new_cost
        locations_to_be_checked.extend(get_next_locations(check_loc))

pprint(costs_list)
