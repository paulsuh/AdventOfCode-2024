from pprint import pprint
from dataclasses import dataclass
from abc import abstractmethod, ABC
from re import match
from collections import deque

from Inputs.Day24_input import initial_values, gates


# initial_values = """x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1"""
#
# gates = """ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj"""

# initial_values = """x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0"""
#
# gates = """x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02"""


wire_values_dict: dict[str, int] = {
    one_value.split(": ")[0]: int(one_value.split(": ")[1])
    for one_value in initial_values.splitlines()
}

pprint(wire_values_dict)

@dataclass
class Gate(ABC):
    operand_1: str
    operand_2: str
    destination: str

    @abstractmethod
    def core_operation(self, v1: int, v2: int) -> int:
        pass

    def check_gate(self) -> bool:
        try:
            v1 = wire_values_dict[self.operand_1]
            v2 = wire_values_dict[self.operand_2]
            wire_values_dict[self.destination] = self.core_operation(v1, v2)
            return True
        except KeyError:
            # values not ready yet
            return False


class AndGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 & v2


class OrGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 | v2


class XorGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 ^ v2


def wires_to_value(wire_values: dict[str, int]) -> int:
    z_keys = [
        one_key
        for one_key in wire_values.keys()
        if one_key.startswith("z")
    ]
    z_keys.sort(reverse=True)
    print(z_keys)

    result = 0
    for one_key in z_keys:
        result = (result << 1) + wire_values[one_key]
    return result


gates_list: deque[Gate] = deque()

for one_gate in gates.splitlines():
    gate_items = match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", one_gate)
    match gate_items[2]:
        case "AND":
            gates_list.append(AndGate(gate_items[1], gate_items[3], gate_items[4]))
        case "OR":
            gates_list.append(OrGate(gate_items[1], gate_items[3], gate_items[4]))
        case "XOR":
            gates_list.append(XorGate(gate_items[1], gate_items[3], gate_items[4]))

pprint(gates_list)


while len(gates_list) > 0:
    current_gate = gates_list.popleft()
    if not current_gate.check_gate():
        # gate did not fire so put it back on the list
        gates_list.append(current_gate)


pprint(wire_values_dict)
z = wires_to_value(wire_values_dict)
print(z)
