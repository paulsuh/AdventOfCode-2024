from pprint import pprint
from collections import deque
from operator import add, xor

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

# problem_input = """AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA"""

# problem_input = """EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE"""

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
            sides = count_corners_for_region(one_region)
            area = len(one_region)
            cost = sides * area
            print(f"{one_crop}: {area} x {sides} = {cost}")
            result += cost
    return result


def calc_boundaries(region: set[tuple[int, int]]
                    ) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    # returns a set of (inside, outside) pairs
    result = set()
    for one_cell in region:
        cell_row, cell_col = one_cell
        if (cell_row-1, cell_col) not in region:
            result.add((one_cell, (cell_row-1, cell_col)))
        if (cell_row, cell_col-1) not in region:
            result.add((one_cell, (cell_row, cell_col-1)))
        if (cell_row, cell_col+1) not in region:
            result.add((one_cell, (cell_row, cell_col+1)))
        if (cell_row+1, cell_col) not in region:
            result.add((one_cell, (cell_row+1, cell_col)))
    return result


outside_corner_patterns = (
    #    f       f
    ((-1, 0), (0, -1)),     # upper left
    ((-1, 0), (0, 1)),      # upper right
    ((1, 0), (0, 1)),       # lower right
    ((1, 0), (0, -1))       # lower left
)

def check_outside_corners_for_cell(cell: tuple[int, int], region: set[tuple[int, int]]) -> int:
    result = 0
    for one_pattern in outside_corner_patterns:
        check = all(
            tuple(map(add, cell, one_offset)) not in region
            for one_offset in one_pattern
        )
        # print(check)
        result += 1 if check else 0
    return result


inside_corner_patterns = (
    #   t       t        f
    ((-1, 0), (0, -1), (-1, -1)),   # upper left
    ((-1, 0), (0, 1), (-1, 1)),     # upper right
    ((1, 0), (0, 1), (1, 1)),       # lower right
    ((1, 0), (0, -1), (1, -1))      # lower left
)
def check_inside_corners_for_cell(cell: tuple[int, int], region: set[tuple[int, int]]) -> int:
    result = 0
    for one_pattern in inside_corner_patterns:
        check = (
            tuple(map(add, cell, one_offset)) in region
            for one_offset in one_pattern
        )
        check2 = all(map(xor, check, (False, False, True)))
        result += 1 if check2 else 0
    return result


def count_corners_for_region(region: set[tuple[int, int]]) -> int:
    corners = (
        check_outside_corners_for_cell(one_cell, region) + \
        check_inside_corners_for_cell(one_cell, region)
        for one_cell in region
    )
    return sum(corners)


r = get_all_crop_regions()
pprint(r)

# print(r["A"][0])
# outside_count = check_outside_corners_for_cell((0, 3), r["A"][0])
# print(outside_count)
# inside_count = check_inside_corners_for_cell((0, 3), r["A"][0])
# print(inside_count)
# region_count = count_corners_for_region(r["D"][0])
# print(region_count)
print(calc_fence_price(r))
# b = calc_boundaries(r["O"][0])
# pprint(b)

# mm = split_input(problem_input)
# pprint(mm)
# # r = flood_fill("I", mm, (5, 2))
# # print(sorted(r))
# a = get_regions_for_type("R", mm)
# print(a)
# p = perimeter_for_region(a[0])
# print(p)
