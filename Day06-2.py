from pprint import pprint

from Inputs.Day06_input import problem_input
from operator import add


# problem_input = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#..."""

# problem_input = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#..."""

# problem_input = """....#..#..
# .........#
# .#..^...#.
# ........#.
# #.........
# ......#..."""

problem_map = problem_input.splitlines()

for row_num, row in enumerate(problem_map):
    if (initial_guard_col := row.find("^")) >= 0:
        initial_guard_loc = (row_num, initial_guard_col, -1, 0)
        break
    if (initial_guard_col := row.find(">")) >= 0:
        initial_guard_loc = (row_num, initial_guard_col, 0, 1)
        break
    if (initial_guard_col := row.find("v")) >= 0:
        initial_guard_loc = (row_num, initial_guard_col, 1, 0)
        break
    if (initial_guard_col := row.find("<")) >= 0:
        initial_guard_loc = (row_num, initial_guard_col, 0, 1)
        break


print(len(problem_map), len(problem_map[0]))
# pprint(problem_map)
# print(initial_guard_loc)

dir_rotation_dict = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)
}


def find_next_loc_dir(current_loc: tuple[int, int, int, int], current_map: list[str]) -> tuple[int, int, int, int]:
    # returns new_loc, new_dir
    new_dir = (current_loc[2], current_loc[3])
    for i in range(3):
        new_loc_row = current_loc[0] + new_dir[0]
        new_loc_col = current_loc[1] + new_dir[1]
        if new_loc_row < 0 or new_loc_row >= len(current_map) or new_loc_col < 0 or new_loc_col >= len(current_map[0]):
            raise IndexError("Guard exited map")
        if current_map[new_loc_row][new_loc_col] != "#":
            return new_loc_row, new_loc_col, new_dir[0], new_dir[1]
        new_dir = dir_rotation_dict[new_dir]
    raise RuntimeError(f"can't find next step {current_loc}")


first_time = True


def run_guard_path(updated_map: list[str]) -> int | set:

    global first_time

    guard_loc = initial_guard_loc

    # print(f"starting at {guard_loc} {guard_dir}")
    guard_locations_dirs = set()
    try:
        while (0 <= guard_loc[0] < len(problem_map)) and  (0 <= guard_loc[1] < len(problem_map[0])):

            guard_loc = find_next_loc_dir(guard_loc, updated_map)
            if guard_loc in guard_locations_dirs:
                # print(f"loop at {guard_loc} after {len(guard_locations_dirs)} steps")
                # pprint(guard_locations_dirs)
                return 1
            # print(guard_loc, guard_dir)
            guard_locations_dirs.add(guard_loc)
    except RuntimeError as r_e:
        raise r_e
    except Exception:
        print(f"exception at {guard_loc}")
        pass
    # pprint(guard_locations_dirs)
    # print(len(guard_locations_dirs))
    if first_time:
        first_time = False
        return guard_locations_dirs
    else:
        return 0


possible_blocks = run_guard_path(problem_map)
# pprint(problem_map)


loop_points = set()
for pb in possible_blocks:
    if problem_map[pb[0]][pb[1]] == ".":
        new_map = problem_map.copy()
        tmp_row = list(new_map[pb[0]])
        tmp_row[pb[1]] = "#"
        new_map[pb[0]] = "".join(tmp_row)
        is_loop = run_guard_path(new_map)
        if is_loop == 1:
            loop_points.add((pb[0], pb[1]))
            # pprint(new_map)

print(loop_points)
print(len(loop_points))

pprint(f"out of bounds {[x for x in loop_points if x[0] >= 130 or x[1] >= 130]}")
