from pprint import pprint

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


def count_prefixes(remaining_stripes: str) -> list[str]:
    result = []
    for one_towel in available_towels:
        if remaining_stripes == one_towel:
            result.append(one_towel)
        elif remaining_stripes.startswith(one_towel):
            possible_endings = count_prefixes(remaining_stripes[len(one_towel):])
            possible_sequences = [
                f"{one_towel}.{one_ending}"
                for one_ending in possible_endings
            ]
            result += possible_sequences
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


number_of_possible_patterns = 0
for one_pattern in desired_patterns_list:
    pattern_possible = can_match_prefixes(one_pattern)
    print(pattern_possible, one_pattern)
    if pattern_possible:
        number_of_possible_patterns += 1

print(number_of_possible_patterns)
