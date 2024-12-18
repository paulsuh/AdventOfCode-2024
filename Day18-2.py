from pprint import pprint
from collections import deque
from typing import NamedTuple
from operator import add

from Inputs.Day18_input import problem_input, map_height, map_width, num_blocks


class Location(NamedTuple):
    row: int
    col: int


# problem_input = """5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0"""
#
# map_height = 7
# map_width = 7
# num_blocks = 12


blocks_lines = [
    one_line.split(",")
    for one_line in problem_input.splitlines()
]

full_block_list = [
    (int(y), int(x))
    for x, y in blocks_lines
]


next_location_offsets = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
)


def get_next_locations(start_loc: Location, block_list: list[Location]) -> list[Location]:
    result = []
    for one_offset in next_location_offsets:
        if (next_loc := Location(*map(add, start_loc, one_offset))) not in block_list:
            result.append(next_loc)
    return result


def get_costs_for_next_locations(start_loc: Location, block_list: list[Location],
                                 location_cost: dict[Location, int]) -> list[Location]:
    next_locations = get_next_locations(start_loc, block_list)
    result = []
    current_loc_cost = location_cost.setdefault(start_loc, map_width*map_height + 1)
    for one_next_loc in next_locations:
        next_loc_cost = current_loc_cost + 1
        if next_loc_cost < location_cost.setdefault(one_next_loc, map_width*map_height + 1):
            location_cost[one_next_loc] = next_loc_cost
            result.append(one_next_loc)

    return result


# x = get_costs_for_next_locations(Location(0, 0))
# print(x)
# pprint(location_cost)

def check_for_path(block_num: int) -> bool:
    locations_to_be_checked: deque[Location] = deque()
    locations_to_be_checked.append(Location(0, 0))

    block_list = full_block_list[:block_num+1]
    block_list += [
        (y, map_width)
        for y in range(map_height)
    ]
    block_list += [
        (y, -1)
        for y in range(map_height)
    ]
    block_list += [
        (map_height, x)
        for x in range(map_width)
    ]
    block_list += [
        (-1, x)
        for x in range(map_width)
    ]
    location_cost: dict[Location, int] = {
        Location(0, 0): 0
    }

    while len(locations_to_be_checked) > 0:
        current_loc = locations_to_be_checked.popleft()

        next_locations = get_costs_for_next_locations(current_loc, block_list, location_cost)
        locations_to_be_checked.extend(next_locations)

    # pprint(location_cost)
    return (map_height - 1, map_width - 1) in location_cost.keys()


for last_block_falling in range(len(full_block_list)-1, 0, -1):
    print(full_block_list[last_block_falling])
    if check_for_path(last_block_falling):
        print("path found")
        print(",".join(
            [
                str(x)
                for x in reversed(full_block_list[last_block_falling+1])
            ]))
        break
