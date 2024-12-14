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


robots_list = []
for one_robot in problem_input.splitlines():
    r = match(r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", one_robot)
    robots_list.append(
        [int(r[2]), int(r[1]), int(r[4]), int(r[3])]
    )

pprint(robots_list)

for one_turn in range(100):
    for one_robot in robots_list:
        new_r = (one_robot[0] + one_robot[2]) % map_height
        new_c = (one_robot[1] + one_robot[3]) % map_width
        one_robot[0] = new_r
        one_robot[1] = new_c


quadrants = [0, 0, 0, 0]
for one_robot in robots_list:
    if 0 <= one_robot[0] < map_height // 2 and \
            0 <= one_robot[1] < map_width // 2:
        quadrants[0] += 1
    elif 0 <= one_robot[0] < map_height // 2 and \
            map_width // 2 < one_robot[1]:
        quadrants[1] += 1
    elif map_height // 2 < one_robot[0] and \
            0 <= one_robot[1] < map_width // 2:
        quadrants[2] += 1
    elif map_height // 2 < one_robot[0] and \
            map_width // 2 < one_robot[1]:
        quadrants[3] += 1

result = prod(quadrants)
print(result)
# end_matrix = [
#     [
#         0
#         for c in range(map_width)
#     ]
#     for r in range(map_height)
# ]
#
# for one_robot in robots_list:
#     end_matrix[one_robot[0]][one_robot[1]] += 1
#
# end_matrix_strings = [
#     "".join([
#         "." if one_cell == 0 else str(one_cell)
#         for one_cell in one_row
#     ])
#     for one_row in end_matrix
# ]
# pprint(end_matrix_strings)

