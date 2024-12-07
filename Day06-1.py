from Inputs.Day06_input import problem_input
from operator import add


problem_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


problem_map = problem_input.splitlines()


for row_num, row in enumerate(problem_map):
    if (guard_col := row.find("^")) >= 0:
        guard_loc = (row_num, guard_col)
        guard_dir = (-1, 0)
        break
    if (guard_col := row.find(">")) >= 0:
        guard_loc = (row_num, guard_col)
        guard_dir = (0, 1)
        break
    if (guard_col := row.find("v")) >= 0:
        guard_loc = (row_num, guard_col)
        guard_dir = (1, 0)
        break
    if (guard_col := row.find("<")) >= 0:
        guard_loc = (row_num, guard_col)
        guard_dir = (0, -1)
        break


print(guard_loc, guard_dir)


guard_locations = set()
try:
    while (0 <= guard_loc[0] < len(problem_map)) and  (0 <= guard_loc[1] < len(problem_map[0])):

        next_loc = tuple(map(add, guard_loc, guard_dir))
        print(next_loc)
        if problem_map[next_loc[0]][next_loc[1]] == "#":
            match guard_dir:
                case (-1, 0):
                    guard_dir = (0, 1)
                case (0, 1):
                    guard_dir = (1, 0)
                case (1, 0):
                    guard_dir = (0, -1)
                case (0, -1):
                    guard_dir = (-1, 0)
            next_loc = tuple(map(add, guard_loc, guard_dir))
            print(guard_dir, next_loc)
        guard_loc = next_loc
        guard_locations.add(next_loc)
except Exception:
    print(f"exception at {guard_loc}, {next_loc}")

print(guard_locations)
print(len(guard_locations))
