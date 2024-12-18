from pprint import pprint

from Inputs.Day15_input import problem_input, robot_moves


# problem_input = """##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########"""
#
# robot_moves = """<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

# problem_input = """########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########"""
#
# robot_moves = """<^^>>>vv<v>>v<<"""


problem_map = [
    [
        one_char
        for one_char in one_line
    ]
    for one_line in problem_input.splitlines()
]

move_matrix = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0)
}

robot_char_pos = problem_input.find("@")
print(robot_char_pos, len(problem_map[0]))
robot_row = problem_input.find("@") // (len(problem_map[0]) + 1)
robot_col = problem_input.find("@") % (len(problem_map[0]) + 1)

print(robot_row, robot_col)


def locate_first_blank_square(start_row: int, start_col: int, row_move: int, col_move: int) -> tuple[int|None, int|None]:

    # go in the direction until you hit a "." or a "#"
    # return the coords of the dot or None
    current_row = start_row
    current_col = start_col
    while True:
        current_row += row_move
        current_col += col_move
        if problem_map[current_row][current_col] == ".":
            return current_row, current_col
        elif problem_map[current_row][current_col] == "#":
            return None, None


def move_robot(start_row: int, start_col: int, end_row: int, end_col: int, row_move: int, col_move: int) -> None:
    problem_map[start_row][start_col] = "."
    problem_map[end_row][end_col] = "O"
    problem_map[start_row + row_move][start_col + col_move] = "@"


for one_move in robot_moves:
    if one_move == "\n":
        continue
    r_move, c_move = move_matrix[one_move]
    dest_row, dest_col = locate_first_blank_square(robot_row, robot_col, r_move, c_move)
    if dest_row is not None:
        move_robot(robot_row, robot_col, dest_row, dest_col, r_move, c_move)
        robot_row += r_move
        robot_col += c_move
    # pprint(problem_map)
    # print()

gps_sum = 0
for row_num, one_row in enumerate(problem_map):
    for col_num, one_cell in enumerate(one_row):
        if one_cell == "O":
            gps_sum += row_num * 100 + col_num

print(gps_sum)
