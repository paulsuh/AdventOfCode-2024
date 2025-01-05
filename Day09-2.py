from operator import itemgetter
from pprint import pprint
from itertools import accumulate, pairwise

from Inputs.Day09_input import problem_input


# problem_input = """2333133121414131402"""
# 00...111...2...333.44.5555.6666.777.888899
# 00992111777.44.333....5555.6666.....8888..
# 00
#   18
#    27
#     8
#      5
#       6
#        7
#         56
#          63
#           70
#             48
#              52
#                45
#                 48
#                  51
#                       110
#                        115
#                         120
#                          125
#                            162
#                             168
#                              174
#                               180
#                                     288
#                                      296
#                                       304
#                                        312


# problem_input = """12345"""
# 0..111....22222
#  22   222
# 022111222
# 0
#  24
#    345
#       12
#        14
#         16
# 60

# problem_input = "4230456"
# 0000..1112222.....333333
#     33       3333
# 306


free_dict: dict[int, list[int]] = {}
files_list: list[tuple[int, int]] = []     # start, end
moved_files: dict[tuple[int, int], tuple[int, int]] = {}

chunks_list = [int(x) for x in problem_input]
chunk_bounds = list(accumulate(chunks_list, initial=0))

for chunk_num, chunk_start_end in enumerate(pairwise(chunk_bounds)):
    chunk_start, chunk_end = chunk_start_end
    if chunk_num % 2 == 0:
        # file
        files_list.append(chunk_start_end)
    else:
        # blank
        free_dict.setdefault(chunk_end-chunk_start, []).append(chunk_start)

for one_key in free_dict.keys():
    free_dict[one_key].sort()

pprint(free_dict)
pprint(files_list)


def find_free_slot(file_start: int, file_end: int) -> tuple[int, int] | None:  # start, end
    file_len = file_end - file_start
    # find the smallest blank slot that will fit the file
    blank_sizes = [
        one_size
        for one_size in free_dict.keys()
        if one_size >= file_len
    ]
    possible_slots = [
        (one_slot, one_size)
        for one_size in blank_sizes
        for one_slot in free_dict[one_size]
        if one_slot < file_start
    ]
    if len(possible_slots) > 0:
        possible_slots.sort(key=itemgetter(0))
        selected_slot = possible_slots[0]       # left-most possible slot
        free_dict[selected_slot[1]].remove(selected_slot[0])
        return selected_slot[0], selected_slot[0]+selected_slot[1]
    else:
        return None


def move_file_attempt(file_start: int, file_end: int) -> None:
    file_len = file_end - file_start
    # find the smallest blank slot that will fit the file
    used_slot = find_free_slot(file_start, file_end)
    if used_slot is None:
        return
    # add to moved files for later processing
    moved_files[(file_start, file_end)] = (used_slot[0], used_slot[0]+file_len)
    # if it didn't take up the entire slot, add the unused portion to
    # the free_dict
    if file_len < used_slot[1] - used_slot[0]:
        free_dict.setdefault(used_slot[1] - used_slot[0] - file_len, []).append(used_slot[0]+file_len)


def segment_checksum(start_block: int, end_block: int, file_id_num: int) -> int:
    return ((end_block-1) * end_block - (start_block-1) * start_block) // 2 * file_id_num


files_list_len = len(files_list)
for file_start, file_end in reversed(files_list):
    move_file_attempt(file_start, file_end)

pprint(free_dict)
pprint(moved_files)

checksum = 0
for file_id_num, one_file in enumerate(files_list):
    start, end = one_file if one_file not in moved_files else moved_files[one_file]
    checksum_for_file = segment_checksum(start, end, file_id_num)
    checksum += checksum_for_file

print(checksum)
