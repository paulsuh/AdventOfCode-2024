from pprint import pprint

from Inputs.Day10_input import problem_input


# problem_input = """89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732"""

# problem_input = """012345
# 123456
# 234567
# 345678
# 4.6789
# 56789."""

# problem_input = """..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987...."""

# problem_input = """.....0.
# ..4321.
# ..5..2.
# ..6543.
# ..7..4.
# ..8765.
# ..9...."""

map_matrix = [
    [
        int(one_char) if one_char in "0123456789" else -1
        for one_char in one_line
    ] + [-1]
    for one_line in problem_input.splitlines()
]

map_matrix.append([-1] * len(map_matrix[0]))

pprint(map_matrix)

delta_list = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
)

def dfs(row: int, col: int) -> int:
    if map_matrix[row][col] == 9:
        return 1
    next_elev = map_matrix[row][col] + 1
    possible_paths = (
        (row+delta[0], col+delta[1])
        for delta in delta_list
        if map_matrix[row+delta[0]][col+delta[1]] == next_elev
    )
    num_peaks = 0
    for one_step in possible_paths:
        num_peaks += dfs(*one_step)
    return num_peaks


t = 0
for r in range(len(map_matrix)-1):
    for c in range(len(map_matrix[0])-1):
        if map_matrix[r][c] == 0:
            p = dfs(r, c)
            print(r, c, p)
            t += p

print(t)
