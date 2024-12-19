from operator import itemgetter
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

# problem_input = """#######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######"""
#
# robot_moves = """<vv<<^^<<^^"""
# robot_moves = """<vv<<^"""


def map_expansion(c: str) -> str:
    match c:
        case "#":
            return "##"
        case ".":
            return ".."
        case "O":
            return "[]"
        case "@":
            return "@."
        case "\n":
            return "\n"


widened_problem_input = "".join([
    map_expansion(c)
    for c in problem_input
])
print(widened_problem_input)

problem_map = [
    [
        one_char
        for one_char in one_line
    ]
    for one_line in widened_problem_input.splitlines()
]

move_matrix = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0)
}

robot_char_pos = problem_input.find("@")
print(robot_char_pos, len(problem_map[0]))
robot_row = problem_input.find("@") // (len(problem_map[0])//2 + 1)
robot_col = problem_input.find("@") % (len(problem_map[0])//2 + 1) * 2

print(robot_row, robot_col)
pprint(problem_map, width=120)


class BoxBlockedException(Exception):
    pass

# boxes are identified by the coords of the left half

def check_one_box(start_row: int, start_col: int, row_move: int, col_move: int) -> list[tuple[int, int]]:
    if col_move == 1:
        # move right
        offset = 1 if problem_map[start_row][start_col] == "@" else 2
        match problem_map[start_row][start_col + offset]:
            case ".":
                # ok to move
                return [(start_row, start_col)]
            case "#":
                # not ok to move
                # pprint(problem_map)
                raise BoxBlockedException(f"Box blocked {start_row}, {start_col} -> {start_row}, {start_col + col_move}")
            case "[":
                # check next box
                result = [(start_row, start_col)]
                result += check_one_box(start_row, start_col + offset, row_move, col_move)
                return result
    elif col_move == -1:
        # move left
        match problem_map[start_row][start_col + col_move]:
            case ".":
                # ok to move
                return [(start_row, start_col)]
            case "#":
                # not ok to move
                # pprint(problem_map)
                raise BoxBlockedException(f"Box blocked {start_row}, {start_col} -> {start_row}, {start_col + col_move}")
            case "]":
                # check next box
                result = [(start_row, start_col)]
                result += check_one_box(start_row, start_col - 2, row_move, col_move)
                return result
    else:
        # vertical move, need to check left and right halves
        result = [(start_row, start_col)]
        match problem_map[start_row + row_move][start_col]:
            # check left half of box
            case ".":
                # ok to move, still need to check other half
                pass
            case "#":
                # not ok to move
                # pprint(problem_map)
                raise BoxBlockedException(f"Box blocked {start_row}, {start_col} -> {start_row + row_move}, {start_col}")
            case "[":
                # next box left half
                result += check_one_box(start_row + row_move, start_col, row_move, col_move)
            case "]":
                # next box right half
                result += check_one_box(start_row + row_move, start_col-1, row_move, col_move)
        if problem_map[start_row][start_col] == "[":
            # only check right half if it's a box
            # don't bother if it's the robot
            match problem_map[start_row + row_move][start_col+1]:
                # check right half of box
                case ".":
                    # ok to move, actual movement done later
                    pass
                case "#":
                    # not ok to move
                    # pprint(problem_map)
                    raise BoxBlockedException(f"Box blocked {start_row}, {start_col} -> {start_row + row_move}, {start_col}")
                case "[":
                    # next box left half
                    # don't check for right half as if there is a right half
                    # then the check for the left half took care of it already
                    result += check_one_box(start_row + row_move, start_col + 1, row_move, col_move)
        return result


def move_box(start_row: int, start_col: int, row_move: int, col_move: int) -> None:
    if row_move == 0:
        # horizontal move
        if col_move > 0:
            # moving right
            if problem_map[start_row][start_col + 2 * col_move] != ".":
                # sanity check
                # pprint(problem_map)
                raise RuntimeError(
                    f"Box blocked {start_row}, {start_col} -> {start_row}, {start_col + col_move}")
            problem_map[start_row][start_col + col_move + 1] = ']'
            problem_map[start_row][start_col + col_move] = '['
            # erase current position
            problem_map[start_row][start_col] = '.'
        else:
            # moving left
            if problem_map[start_row][start_col + col_move] != ".":
                # sanity check
                # pprint(problem_map)
                raise RuntimeError(
                    f"Box blocked {start_row}, {start_col} -> {start_row}, {start_col + col_move}")
            problem_map[start_row][start_col + col_move] = '['
            problem_map[start_row][start_col] = ']'
            # erase current position of right half
            problem_map[start_row][start_col + 1] = '.'

    else:
        # vertical move
        if problem_map[start_row + row_move][start_col] != "." or \
                problem_map[start_row + row_move][start_col + 1] != ".":
            # sanity check
            pprint(problem_map)
            raise RuntimeError(f"Box blocked {start_row}, {start_col} -> {start_row}, {start_col + col_move}")
        problem_map[start_row + row_move][start_col] = '['
        problem_map[start_row + row_move][start_col + 1] = ']'

        # erase current position
        problem_map[start_row][start_col] = '.'
        # erase former position of right half
        problem_map[start_row][start_col + 1] = '.'


def move_robot(start_row: int, start_col: int, row_move: int, col_move: int) -> tuple[int, int]:
    try:
        moves = check_one_box(start_row, start_col, row_move, col_move)
        # sort moves by row or col and direction
        match row_move, col_move:
            case 1, 0:
                # move down
                moves.sort(key=itemgetter(0), reverse=True)
            case -1, 0:
                # move up
                moves.sort(key=itemgetter(0))
            case 0, 1:
                # move right
                moves.sort(key=itemgetter(1), reverse=True)
            case 0, -1:
                # move left
                moves.sort(key=itemgetter(1))

        for one_move in moves:
            if problem_map[one_move[0]][one_move[1]] == "[":
                move_box(*one_move, row_move, col_move)
            elif problem_map[one_move[0]][one_move[1]] == "@":
                problem_map[start_row][start_col] = '.'
                problem_map[start_row + row_move][start_col + col_move] = '@'

        return start_row + row_move, start_col + col_move
    except BoxBlockedException:
        # something was blocked, so don't move
        return start_row, start_col


# move_box(3, 6, 0, -1)
# move_box(3, 8, 0, -1)
# move_robot(3, 10, 0, -1)

for one_move in robot_moves:
    if one_move == "\n":
        continue
    r_move, c_move = move_matrix[one_move]
    robot_row, robot_col = move_robot(robot_row, robot_col, r_move, c_move)

print()
pprint(problem_map, width=120)

#     dest_row, dest_col = locate_first_blank_square(robot_row, robot_col, r_move, c_move)
#     if dest_row is not None:
#         move_robot(robot_row, robot_col, dest_row, dest_col, r_move, c_move)
#         robot_row += r_move
#         robot_col += c_move
#     # pprint(problem_map)
#     # print()
#
gps_sum = 0
for row_num, one_row in enumerate(problem_map):
    for col_num, one_cell in enumerate(one_row):
        if one_cell == "[":
            gps_sum += row_num * 100 + col_num

print(gps_sum)
