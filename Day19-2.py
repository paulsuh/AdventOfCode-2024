from pprint import pprint
from functools import cache

from Inputs.Day19_input import available_towels, desired_patterns


# available_towels = """r, wr, b, g, bwu, rb, gb, br"""
#
# desired_patterns = """brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb"""

available_towels_list = available_towels.split(", ")

desired_patterns_list = desired_patterns.splitlines()

print(available_towels_list)
print(desired_patterns_list)


@cache
def count_prefixes(remaining_stripes: str) -> list[str]:
    result = 0
    for i, one_towel in enumerate(available_towels_list):
        if remaining_stripes == one_towel:
            result += 1
        elif remaining_stripes.startswith(one_towel):
            num_possible_endings = count_prefixes(remaining_stripes[len(one_towel):])
            result += num_possible_endings
        else:
            # not a possible next towel
            pass
    return result


def can_match_prefixes(remaining_stripes: str) -> bool:
    for one_towel in available_towels_list:
        if remaining_stripes == one_towel:
            return True
        elif remaining_stripes.startswith(one_towel):
            combo_possible = can_match_prefixes(remaining_stripes[len(one_towel):])
            if combo_possible:
                return True
        else:
            # not a possible next towel
            pass
    return False


number_of_possible_arrangements = 0
for one_pattern in desired_patterns_list:
    arrangements_count = count_prefixes(one_pattern)
    print(arrangements_count, one_pattern)
    number_of_possible_arrangements += arrangements_count

print(number_of_possible_arrangements)
