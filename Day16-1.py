from collections import deque
from typing import NamedTuple
from pprint import pprint

from Inputs.Day16_input import problem_input


# problem_input = """#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################"""


# problem_input = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############"""


# row, col, row_move, col_move
class Location(NamedTuple):
    row: int
    col: int
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


def get_next_locations(loc: Location) -> list[Location]:
    result = []
    for row_move, col_move in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if problem_map[loc.row + row_move][loc.col + col_move] in ".E":
            result.append(Location(loc.row + row_move, loc.col + col_move, row_move, col_move))
    return result


def get_location_cost(old_loc: Location,
                      new_loc: Location,
                      locations_costs: dict[Location, int]
                      ) -> int:    # cost, new Location
    old_loc_cost = locations_costs[old_loc]
    rotation_cost = dir_cost_lookup[(old_loc.row_move, old_loc.col_move,
                                     new_loc.row_move, new_loc.col_move)]
    step_cost = 1
    result = old_loc_cost + rotation_cost + step_cost
    return result


# x = get_next_locations(start_location.row, start_location.column)
# for one_location in x:
#     c = get_location_cost(start_location, one_location)
#     print(one_location, c)


def check_for_paths(start: Location) -> dict[Location, int]:
    locations_to_be_checked: deque[tuple[Location]] = deque()
    locations_to_be_checked.append(start)
    locations_costs: dict[Location, int] = {start: 0}

    # locations_to_be_checked contains locations that have already been
    # costed out and we need to check each of the adjacent cells
    # print(locations_to_be_checked)
    while len(locations_to_be_checked) > 0:
        current_loc = locations_to_be_checked.popleft()
        next_locations = get_next_locations(current_loc)
        for one_next_loc in next_locations:
            next_loc_cost = get_location_cost(current_loc, one_next_loc, locations_costs)
            if locations_costs.setdefault(one_next_loc, 1000000000000000) > next_loc_cost:
                locations_costs[one_next_loc] = next_loc_cost
                locations_to_be_checked.append(one_next_loc)

    return locations_costs


all_location_costs = check_for_paths(start_location)
target_location_costs = {
    one_location: cost
    for one_location, cost in all_location_costs.items()
    if one_location.row == end_row and one_location.col == end_col
}
pprint(target_location_costs)
pprint(min(target_location_costs.values()))
