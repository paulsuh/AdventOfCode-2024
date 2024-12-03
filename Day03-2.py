from re import findall, split
from itertools import pairwise
from more_itertools import flatten

from Inputs.Day03_input import problem_input

# problem_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


chunks_list = split(r"(do\(\)|don't\(\))", problem_input)

good_chunks_list = [
    c2
    for c1, c2 in pairwise(chunks_list)
    if c1 == "do()"
]

all_good_chunks_list = [chunks_list[0]] + good_chunks_list

mul_matches = flatten([
    findall(r"mul\((\d+),(\d+)\)", one_chunk)
    for one_chunk in all_good_chunks_list
])

match_list = findall(r"mul\((\d+),(\d+)\)", problem_input)

result = sum([
    int(x)*int(y)
    for x, y in mul_matches
])

print(result)
