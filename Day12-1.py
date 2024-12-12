from pprint import pprint
from collections import deque

from Inputs.Day12_input import problem_input


# problem_input = """RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE"""

# problem_input = """OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO"""

# problem_input = """AAAA
# BBCD
# BBCC
# EEEC"""


# split in maps by crop type
crop_types = {
    c
    for c in problem_input
    if c != "\n"
}

pprint(crop_types)

def split_input(input_map: str) -> list[list[str]]:
    # Python clever list indexing hack
    # append one additional row and one additional column to allow
    # easy check for cells on the edge. At index 0, left or up
    # becomes index -1, which wraps around to len
    result = [
        [
            c
            for c in one_line
        ] + ["."]
        for one_line in input_map.splitlines()
    ]
    result.append(["."]*len(result[0]))
    return result


def get_regions_for_type(crop_type: str, map_matrix: list[list[str]]) -> list[set[tuple[int, int]]]:
    # run thru the matrix and get one region for the crop type
    result = []

    for row in range(len(map_matrix)):
        for column in range(len(map_matrix[0])):
            if map_matrix[row][column] == crop_type:
                current_region = flood_fill(crop_type, map_matrix, (row, column))
                for one_cell in current_region:
                    map_matrix[one_cell[0]][one_cell[1]] = "."
                result.append(current_region)

    return result


def flood_fill(crop_type: str, map_matrix: list[list[str]], start_cell: tuple[int, int]
               ) -> set[tuple[int, int]]:
    result = set()
    to_be_checked = deque([start_cell])
    while len(to_be_checked) > 0:
        if (current_cell := to_be_checked.popleft()) not in result:
            result.add(current_cell)
            check_row, check_col = current_cell
            if map_matrix[check_row-1][check_col] == crop_type:
                to_be_checked.append((check_row-1, check_col))
            if map_matrix[check_row][check_col-1] == crop_type:
                to_be_checked.append((check_row, check_col-1))
            if map_matrix[check_row][check_col+1] == crop_type:
                to_be_checked.append((check_row, check_col+1))
            if map_matrix[check_row+1][check_col] == crop_type:
                to_be_checked.append((check_row+1, check_col))
    return result


def perimeter_for_region(region: set[tuple[int, int]]) -> int:
    result = 0
    for one_cell in region:
        current_row, current_col = one_cell
        if (current_row-1, current_col) not in region:
            result += 1
        if (current_row, current_col-1) not in region:
            result += 1
        if (current_row, current_col+1) not in region:
            result += 1
        if (current_row+1, current_col) not in region:
            result += 1
    return result


def get_all_crop_regions() -> dict[str, list[set[tuple[int, int]]]]:
    result = {}
    for one_crop in crop_types:
        result[one_crop] = get_regions_for_type(one_crop, split_input(problem_input))
    return result


def calc_fence_price(crops: dict[str, list[set[tuple[int, int]]]]) -> int:
    result = 0
    for one_crop in crops.keys():
        for one_region in crops[one_crop]:
            perimeter = perimeter_for_region(one_region)
            area = len(one_region)
            cost = perimeter * area
            print(f"{one_crop}: {area} x {perimeter} = {cost}")
            result += cost
    return result


r = get_all_crop_regions()
pprint(r)
print(calc_fence_price(r))

# mm = split_input(problem_input)
# pprint(mm)
# # r = flood_fill("I", mm, (5, 2))
# # print(sorted(r))
# a = get_regions_for_type("R", mm)
# print(a)
# p = perimeter_for_region(a[0])
# print(p)


# for one_crop in crop_types:
#     crop_map = [
#         [
#             c if c == one_crop else "."
#             for c in one_line
#         ]
#         for one_line in problem_input.splitlines()
#     ]
#
