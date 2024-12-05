from pprint import pprint
from re import match

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

# problem_input = """.M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# .........."""

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
pprint(word_matrix)

x_mas_patterns = [
    r"^M.M.A.S.S$",
    r"^M.S.A.M.S$",
    r"^S.S.A.M.M$",
    r"^S.M.A.S.M$"
]

number_of_x_mas = 0
for r in range(len(word_matrix)-2):
    for c in range(len(word_matrix)-2):
        possible_x_mas = "".join(word_matrix[r][c:c+3]+word_matrix[r+1][c:c+3]+word_matrix[r+2][c:c+3])
        print(possible_x_mas)
        for one_pattern in x_mas_patterns:
            if match(one_pattern, possible_x_mas):
                number_of_x_mas += 1
                print("^^^^")

print(number_of_x_mas)
