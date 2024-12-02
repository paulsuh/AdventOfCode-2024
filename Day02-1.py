from itertools import pairwise

from more_itertools import sliding_window

from Inputs.Day02_input import levels


# levels = """7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9"""

levels_list = [
    list(map(int, one_line.split()))
    for one_line in levels.splitlines()
]

# print(levels_list)

def is_safe(report: list[int]) -> bool:
    safe_step = [
        True if 1 <= abs(v1 - v2) <= 3 else False
        for v1, v2 in pairwise(report)
    ]
    safe_direction = [
        (v1-v2) * (v2-v3) > 0
        for v1, v2, v3 in sliding_window(report, 3)
    ]
    return all(safe_direction) and all(safe_step)

safe_levels = [
    1
    for x in levels_list
    if is_safe(x)
]

print(sum(safe_levels))
