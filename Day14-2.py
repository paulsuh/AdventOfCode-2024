from pprint import pprint
from re import match
from math import prod

from Inputs.Day14_input import problem_input

map_height = 103
map_width = 101


# problem_input = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3"""
#
# map_height = 7
# map_width = 11
#
# problem_input = """p=4,0 v=1,1
# p=3,1 v=1,1
# p=4,1 v=1,1
# p=5,1 v=1,1
# p=2,2 v=1,1
# p=3,2 v=1,1
# p=4,6 v=1,-1
# p=5,2 v=1,1
# p=6,2 v=1,1"""
#
# map_height = 7
# map_width = 11


def print_map():
    end_matrix = [
        [
            0
            for c in range(map_width)
        ]
        for r in range(map_height)
    ]

    for one_robot in robot_positions_list:
        end_matrix[one_robot[0]][one_robot[1]] += 1

    end_matrix_strings = [
        "".join([
            "." if one_cell == 0 else str(one_cell)
            for one_cell in one_row
        ])
        for one_row in end_matrix
    ]
    pprint(end_matrix_strings)
    print("\n-----------------------------------------\n")


robot_positions_list = []
robot_velocities_list = []
for one_robot in problem_input.splitlines():
    r = match(r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", one_robot)
    robot_positions_list.append(
        [int(r[2]), int(r[1])]
    )
    robot_velocities_list.append(
        (int(r[4]), int(r[3]))
    )

# pprint(robots_list)
# print_map()


# look for offsets of
#       1,-1  1,0  1,1
# 2,-2  2,-2  2,0  2,1  2,2
# halt if we see this
possible_offsets = (
    (1, -1),
    (1, 0),
    (1, 1),
    (2, -2),
    (2, -1),
    (2, -0),
    (2, 1),
    (2, 2)
)
def check_robot_for_possible_christmas_tree(row: int, col: int) -> bool:
    for row_offset, col_offset in possible_offsets:
        if [row+row_offset, col+col_offset] not in robot_positions_list:
            return False
    return True


def check_robots_for_tree() -> bool:
    for one_robot in robot_positions_list:
        if check_robot_for_possible_christmas_tree(*one_robot):
            print_map()
            return True
    return False


for one_turn in range(10000):
    for index, one_robot in enumerate(robot_positions_list):
        new_r = (one_robot[0] + robot_velocities_list[index][0]) % map_height
        new_c = (one_robot[1] + robot_velocities_list[index][1]) % map_width
        one_robot[0] = new_r
        one_robot[1] = new_c
    if one_turn % 100 == 0:
        print(".", end="")

    if check_robots_for_tree():
        print(one_turn+1)
        break

# print_map()