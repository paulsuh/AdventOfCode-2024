from functools import cmp_to_key
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

def comparison_func(a, b) -> int:
    if b in rules_dict.get(a, []):
        return -1
    elif a in rules_dict.get(b, []):
        return 1
    else:
        return 0


middle_page_sum = 0
for one_page_set in page_sets:
    sorted_list = sorted(one_page_set, key=cmp_to_key(comparison_func))
    if sorted_list != one_page_set:
        middle_value = sorted_list[len(sorted_list)//2]
        middle_page_sum += middle_value
        print(one_page_set)
        print(sorted_list)
        print(middle_value)

print(middle_page_sum)
