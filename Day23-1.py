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


connections_dict = {}
for one_connection in problem_input.splitlines():
    c1, c2 = one_connection.split("-")
    connections_dict.setdefault(c1, set()).add(c2)
    connections_dict.setdefault(c2, set()).add(c1)

# pprint(connections_dict)


# lan_parties_list: set[tuple[str, str, str]] = set()
lan_parties_count = 0
for one_computer, connecting_computers in connections_dict.items():
    for other_comp_1, other_comp_2 in combinations(connecting_computers, 2):
        if other_comp_2 in connections_dict[other_comp_1]:
            if one_computer[0] == "t" or other_comp_1[0] == "t" or other_comp_2[0] == "t":
                lan_parties_count += 1
            # lan_party: list[str] = [one_computer, other_comp_1, other_comp_2]
            # lan_party.sort()
            # lan_parties_list.add((lan_party[0], lan_party[1], lan_party[2]))

pprint(lan_parties_count // 3)

