from itertools import batched, product
from more_itertools import transpose
from pprint import pprint
from operator import add

from Inputs.Day25_input import problem_input


# problem_input = """#####
# .####
# .####
# .####
# .#.#.
# .#...
# .....
#
# #####
# ##.##
# .#.##
# ...##
# ...#.
# ...#.
# .....
#
# .....
# #....
# #....
# #...#
# #.#.#
# #.###
# #####
#
# .....
# .....
# #.#..
# ###..
# ###.#
# ###.#
# #####
#
# .....
# .....
# .....
# #....
# #.#..
# #.#.#
# #####"""


problem_array = problem_input.splitlines()
keys = []
locks = []


for one_chunk in batched(problem_array, 8):
    actual_chunk = one_chunk[:7]
    if actual_chunk[0] == "#####":
        # lock
        lock_chunk = transpose(actual_chunk[1:])
        lock_final = [
            "".join(one_position)
            for one_position in lock_chunk
        ]
        # print("lock")
        # pprint(lock_final, width=10)
        lock_val = tuple(
            one_position.index(".")
            for one_position in lock_final
        )
        print(lock_val)
        locks.append(lock_val)
    else:
        # key
        key_chunk = transpose(reversed(actual_chunk[:6]))
        key_final = [
            "".join(one_position)
            for one_position in key_chunk
        ]
        # print("key")
        # pprint(key_final, width=10)
        key_val = tuple(
            one_position.index(".")
            for one_position in key_final
        )
        print(key_val)
        keys.append(key_val)


def compare_lock_and_key(lock: tuple[int, ...], key: tuple[int, ...]) -> bool:
    return max(map(add, lock, key)) <= 5


print(compare_lock_and_key(locks[0], keys[0]))
x = [
    compare_lock_and_key(l, k)
    for l, k in product(locks, keys)
]
pprint(x)
pprint(sum(x))
