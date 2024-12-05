from pprint import pprint
from typing import Iterator
from re import findall

from Inputs.Day04_input import problem_input

# problem_input = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""

# problem_input = """..........
# ...S..S..S
# ..A....A.A
# .M......MM
# XMAS..SAMX
# MM......M.
# A.A....A..
# S..S..S...
# ..........
# .........."""

word_matrix = [
    [c for c in one_line]
    for one_line in problem_input.splitlines()
]

# print(len(word_matrix), len(word_matrix[0]))
# pprint(word_matrix)


def rotate_90_clockwise(orig_matrix: list[list[str]]) -> list[list[str]]:
    return [list(row) for row in zip(*reversed(orig_matrix))]


#   row     col     d
#   0       4       0
#   0       3       1
#   0       2       2
#   0       1       3
#   0       0       4
#   1       0       5
#   2       0       6
#   3       0       7
#   4       0       8
# d-len+1  len-d-1
def sweep_45_clockwise(orig_matrix: list[list[str]]) -> Iterator[list[str]]:
    for start_col in range(len(orig_matrix)-1, -1, -1):
        current_diag = []
        for current_col in range(start_col, len(orig_matrix)):
            current_row = current_col - start_col
            current_diag.append(orig_matrix[current_row][current_col])
            # print(current_row, current_col)
        # print(start_col-start_col, start_col, len(orig_matrix)-start_col, len(orig_matrix), current_diag)
        yield current_diag

    for start_row in range(1, len(orig_matrix)):
        current_diag = []
        for current_row in range(start_row, len(orig_matrix)):
            current_col = current_row - start_row
            current_diag.append(orig_matrix[current_row][current_col])
            # print(current_row, current_col)
        yield current_diag
        # print(start_row, start_row-start_row, len(orig_matrix), len(orig_matrix)-start_row, current_diag)

    # for diag_num in range(len(orig_matrix)*2):
    #     start_row = max(diag_num - len(orig_matrix) - 1, 0)
    #     end_row = min(diag_num + 1, len(orig_matrix))
    #     start_col = max(len(orig_matrix) - diag_num - 1, 0)
    #     current_diag = []
    #     for row in range(start_row, end_row):
    #         col = start_col + row - start_row
    #         print(row, col)
    #         current_diag.append(orig_matrix[row][col])
    #     print(start_row, start_col, end_row, current_diag)
    #     yield current_diag


# for one_diag in sweep_45_clockwise(word_matrix):
#     pass
#     print(one_diag)

xmas_count = 0
for one_rot in range(4):
    # print("".join(word_matrix[0]))
    for row_num, one_row in enumerate(word_matrix):
        xmas_count += len(findall("XMAS", "".join(one_row)))
        print(row_num, findall("XMAS", "".join(one_row)), "".join(one_row))
    for diag_num, one_diag in enumerate(sweep_45_clockwise(word_matrix)):
        xmas_count += len(findall("XMAS", "".join(one_diag)))
        print(diag_num, findall("XMAS", "".join(one_diag)), "".join(one_diag))
    word_matrix = rotate_90_clockwise(word_matrix)

print(xmas_count)
