from pprint import pprint
from itertools import combinations

from Inputs.Day23_input import problem_input


# problem_input = """kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn"""


def set_to_str(in_set: set[str]) -> str:
    comp_list = list(in_set)
    comp_list.sort()
    result = ",".join(comp_list)
    return result


def str_to_set(in_str: str) -> set[str]:
    result = set(in_str.split(","))
    return result


connections_dict = {}
connected_sets_set: set[str] = set()
for one_connection in problem_input.splitlines():
    c1, c2 = one_connection.split("-")
    connections_dict.setdefault(c1, set()).add(c2)
    connections_dict[c1].add(c1)
    connections_dict.setdefault(c2, set()).add(c1)
    connections_dict[c2].add(c2)
    connected_sets_set.add(set_to_str({c1, c2}))

# pprint(connections_dict)
# pprint(connected_sets_set)


computers_to_check = list(connections_dict.keys())
while len(computers_to_check) > 0:
    current_comp = computers_to_check.pop()
    lan_parties_to_check = list(connected_sets_set)
    for one_lan_party in lan_parties_to_check:
        check_set = str_to_set(one_lan_party)
        if check_set <= connections_dict[current_comp]:
            check_set.add(current_comp)
        connected_sets_set.remove(one_lan_party)
        connected_sets_set.add(set_to_str(check_set))

pprint(connected_sets_set)

result_set = None
result_len = 0
for one_lan_party in connected_sets_set:
    if len(one_lan_party) > result_len:
        result_len = len(one_lan_party)
        result_set = one_lan_party

print(result_len, result_set)
