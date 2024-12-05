from itertools import pairwise
from pprint import pprint
from Inputs.Day05_input import rules, pages

# rules = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13"""
#
# pages = """75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47"""

page_sets = [
    list(map(int, one_line.split(",")))
    for one_line in pages.splitlines()
]
pprint(page_sets)

rules_list = [
    list(map(int, one_line.split("|")))
    for one_line in rules.splitlines()
]
rules_dict = {}
for one_rule in rules_list:
    rules_dict.setdefault(one_rule[0], []).append(one_rule[1])
pprint(rules_dict)

middle_page_sum = 0
for one_page_set in page_sets:
    try:
        for page_index in range(len(one_page_set)):
            lhs = one_page_set[:page_index]
            rhs = one_page_set[page_index+1:]
            right_page_list = rules_dict.get(one_page_set[page_index], [])
            for one_page_to_right in right_page_list:
                if one_page_to_right in lhs:
                    raise ValueError(f"{one_page_to_right} to the left of {one_page_set[page_index]}")
    except ValueError as v:
        print(v)
    else:
        # everything ok to here
        middle_value = one_page_set[len(one_page_set)//2]
        middle_page_sum += middle_value
        print(one_page_set)
        print(middle_value)

print(middle_page_sum)
