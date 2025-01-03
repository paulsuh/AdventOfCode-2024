from operator import add
from pprint import pprint
from itertools import accumulate, pairwise

from Inputs.Day09_input import problem_input


# problem_input = """2333133121414131402"""
# 00...111...2...333.44.5555.6666.777.888899
# 0099811188827773336446555566..............


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

chunks_list = [int(x) for x in problem_input]
chunk_bounds = list(accumulate(chunks_list, initial=0))

print(chunks_list)
print(chunk_bounds)


class CompactionCompleteException(Exception):
    def __init__(self, file_id_number: int = 0, start_block: int = 0, end_block: int = 0):
        self.file_id_number = file_id_number
        self.start_block = start_block
        self.end_block = end_block


# def get_next_empty_block(current_empty_chunk: int, position_within_chunk: int) -> tuple[int, int]:
#     next_position = position_within_chunk + 1
#     if chunk_bounds[current_empty_chunk] + next_position  < chunk_bounds[current_empty_chunk + 1]:
#         return current_empty_chunk, next_position
#     else:
#         return get_next_empty_block(current_empty_chunk + 2, -1)
#
#
# def get_next_file_block(current_file_chunk: int, position_within_chunk: int) -> tuple[int, int]:
#     next_position = position_within_chunk - 1
#     if next_position >= 0:
#         return current_file_chunk, next_position
#     else:
#         return current_file_chunk - 2, chunks_list[current_file_chunk - 2] - 1
#
#
# def physical_block_from_chunk_and_offset(chunk_number: int, position_within_chunk: int) -> int:
#     return chunk_bounds[chunk_number] + position_within_chunk
#
#
# print(get_next_empty_block(1, 2))
# print(get_next_file_block(4, 0))
# print(physical_block_from_chunk_and_offset(4, 0))
# print(physical_block_from_chunk_and_offset(2, 2))


current_forward_index = 0   # block that will be indexed this round
current_forward_chunk = 0
current_forward_chunk_end = chunk_bounds[1]
current_back_index = chunk_bounds[-1]     # block that will be moved this round
current_back_chunk = len(chunks_list) - 1


def segment_checksum(start_block: int, end_block: int, file_id_num: int) -> int:
    return ((end_block-1) * end_block - (start_block-1) * start_block) // 2 * file_id_num


def process_file_forward(file_start: int, file_end: int) -> int:
    global current_forward_chunk

    file_id_num = current_forward_chunk // 2
    # process one file going forward
    # returns the index value
    if file_end < current_back_index:
        checksum_result = segment_checksum(file_start, file_end, file_id_num)
        return checksum_result
    else:
        raise CompactionCompleteException(
            file_id_number=file_id_num,
            start_block=file_start,
            end_block=current_back_index
        )


def relocate_next_file_chunk(max_number_of_blocks: int) -> tuple[int, int]:
    global current_back_chunk, current_back_index

    # returns the number of blocks in the chunk and the file_id_num
    # NOTE: We never have to check whether we hit the forward index, as the
    # forward index will always be either in a free space or at the start of
    # a file chunk
    file_id_result = current_back_chunk // 2
    if max_number_of_blocks < (current_back_index - chunk_bounds[current_back_chunk]):
        # can fill that many chunks from currently moving file
        current_back_index -= max_number_of_blocks
        return max_number_of_blocks, file_id_result
    else:
        # run out of blocks, return remaining blocks
        # then move the chunk pointer
        number_of_blocks_returned = current_back_index - chunk_bounds[current_back_chunk]
        current_back_chunk -= 2
        current_back_index = chunk_bounds[current_back_chunk + 1]
        return number_of_blocks_returned, file_id_result


def process_blank_forward(blank_start: int, blank_end: int) -> int:
    # process one blank chunk
    checksum_result = 0
    current_process_index = blank_start
    while current_process_index < blank_end:
        num_blocks, file_id_num = relocate_next_file_chunk(blank_end - current_process_index)
        new_index = current_process_index + num_blocks
        if new_index >= current_back_index:
            # ran out of blocks in the middle of a blank
            raise CompactionCompleteException(
                file_id_number=file_id_num,
                start_block=current_process_index,
                end_block=new_index
            )
        checksum_result += segment_checksum(current_process_index, new_index, file_id_num)
        current_process_index = new_index
    return checksum_result



print(current_forward_chunk)
print(current_forward_index)
print(current_forward_chunk_end)
print(current_back_chunk)
print(current_back_index)

try:
    checksum_total = 0
    for current_forward_chunk, chunk_start_end in enumerate(pairwise(chunk_bounds)):
        chunk_start, chunk_end = chunk_start_end
        if current_forward_chunk % 2 == 0:
            result1 = process_file_forward(chunk_start, chunk_end)
            checksum_total += result1
        else:
            result2 = process_blank_forward(chunk_start, chunk_end)
            checksum_total += result2
except CompactionCompleteException as cce:
    checksum_cce = segment_checksum(cce.start_block, cce.end_block, cce.file_id_number)
    checksum_total += checksum_cce


print(f"checksum = {checksum_total}")


# both ways tests
# x1 = process_file_forward(current_forward_index, current_forward_chunk_end)
# print(x1)
# current_forward_chunk += 1
# current_forward_index = chunk_bounds[current_forward_chunk]
# current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
# print(current_forward_chunk)
# print(current_forward_index)
# print(current_forward_chunk_end)
# print(current_back_chunk)
# print(current_back_index)
# print("----------")
# x2 = process_blank_forward(current_forward_index, current_forward_chunk_end)
# print(x2)
# current_forward_chunk += 1
# current_forward_index = chunk_bounds[current_forward_chunk]
# current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
# print(current_forward_chunk)
# print(current_forward_index)
# print(current_forward_chunk_end)
# print(current_back_chunk)
# print(current_back_index)
# print("----------")
# x3 = process_file_forward(current_forward_index, current_forward_chunk_end)
# print(x3)
# current_forward_chunk += 1
# current_forward_index = chunk_bounds[current_forward_chunk]
# current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
# print(current_forward_chunk)
# print(current_forward_index)
# print(current_forward_chunk_end)
# print(current_back_chunk)
# print(current_back_index)
# print("----------")
# x4 = process_blank_forward(current_forward_index, current_forward_chunk_end)
# print(x4)
# current_forward_chunk += 1
# current_forward_index = chunk_bounds[current_forward_chunk]
# current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
# print(current_forward_chunk)
# print(current_forward_index)
# print(current_forward_chunk_end)
# print(current_back_chunk)
# print(current_back_index)
# print("----------")
# x5 = process_file_forward(current_forward_index, current_forward_chunk_end)
# print(x5)
# current_forward_chunk += 1
# current_forward_index = chunk_bounds[current_forward_chunk]
# current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
# print(current_forward_chunk)
# print(current_forward_index)
# print(current_forward_chunk_end)
# print(current_back_chunk)
# print(current_back_index)
# print("----------")
# try:
#     x6 = process_blank_forward(current_forward_index, current_forward_chunk_end)
#     print(x6)
#     current_forward_chunk += 1
#     current_forward_index = chunk_bounds[current_forward_chunk]
#     current_forward_chunk_end = chunk_bounds[current_forward_chunk + 1]
#     print(current_forward_chunk)
#     print(current_forward_index)
#     print(current_forward_chunk_end)
#     print(current_back_chunk)
#     print(current_back_index)
#     print("----------")
# except CompactionCompleteException as cce:
#     print("cce-----")
#     print(cce.file_id_number)
#     print(cce.start_block)
#     print(cce.end_block)
#     print(segment_checksum(cce.start_block, cce.end_block, cce.file_id_number))


# forward tests
# try:
#     current_back_index = 18
#
#     print(current_forward_chunk)
#     print(current_forward_index)
#     print(current_forward_chunk_end)
#     print(process_file_forward(current_forward_index, current_forward_chunk_end))
#     print("----------")
#     print(current_forward_chunk)
#     print(current_forward_index)
#     print(current_forward_chunk_end)
#     print(process_file_forward(current_forward_index, current_forward_chunk_end))
#     print("----------")
#     print(current_forward_chunk)
#     print(current_forward_index)
#     print(current_forward_chunk_end)
#     print(process_file_forward(current_forward_index, current_forward_chunk_end))
#     print("----------")
#     print(current_forward_chunk)
#     print(current_forward_chunk_end)
#     print(current_forward_index)
#     print(process_file_forward(current_forward_index, current_forward_chunk_end))
#     print("----------")
#     print(current_forward_chunk)
#     print(current_forward_chunk_end)
#     print(current_forward_index)
#
# except CompactionCompleteException as cce:
#     print("cce-----")
#     print(cce.file_id_number)
#     print(cce.start_block)
#     print(cce.end_block)
#     print(segment_checksum(cce.start_block, cce.end_block, cce.file_id_number))


# current_source_block = len(problem_input) - 1
# current_target_file_remaining_len = int(problem_input[current_source_block])
# current_dest_block = int(problem_input[0])
#
