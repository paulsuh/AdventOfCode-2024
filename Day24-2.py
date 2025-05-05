from pprint import pprint
from dataclasses import dataclass, field
from abc import abstractmethod, ABC
from re import match
from collections import deque
from typing import Self

from Inputs.Day24_input import initial_values, gates


# initial_values = """x00: 0
# x01: 1
# x02: 0
# x03: 1
# x04: 0
# x05: 1
# y00: 0
# y01: 0
# y02: 1
# y03: 1
# y04: 0
# y05: 1"""
#
# gates = """x00 AND y00 -> z05
# x01 AND y01 -> z02
# x02 AND y02 -> z01
# x03 AND y03 -> z03
# x04 AND y04 -> z04
# x05 AND y05 -> z00"""


wire_values_dict: dict[str, int] = {
    one_value.split(": ")[0]: int(one_value.split(": ")[1])
    for one_value in initial_values.splitlines()
}
wire_dependencies = {
    wire: set()
    for wire in wire_values_dict.keys()
}

# pprint(wire_values_dict)

@dataclass
class Gate(ABC):
    operand_1: str
    operand_2: str
    destination: str

    @abstractmethod
    def core_operation(self, v1: int, v2: int) -> int:
        pass

    @property
    @abstractmethod
    def operation_type(self) -> int:
        pass

    def __hash__(self):
        return hash((self.operand_1, self.operand_2, self.destination, self.operation_type))

    def check_gate(self, values: dict[str, int], dependencies: dict[str, set[Self]]) -> bool:
        try:
            v1 = values[self.operand_1]
            v2 = values[self.operand_2]
            values[self.destination] = self.core_operation(v1, v2)
            dependencies.setdefault(self.destination, set()).add(self)
            dependencies[self.destination].update(dependencies.setdefault(self.operand_1, set()))
            dependencies[self.destination].update(dependencies.setdefault(self.operand_2, set()))
            return True
        except KeyError:
            # values not ready yet
            return False


class AndGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 & v2

    def operation_type(self):
        return 0


class OrGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 | v2

    def operation_type(self):
        return 1


class XorGate(Gate):

    def core_operation(self, v1: int, v2: int) -> int:
        return v1 ^ v2

    def operation_type(self):
        return 2


def wires_to_value(prefix: str, wire_values: dict[str, int]) -> int:
    prefix_keys = [
        one_key
        for one_key in wire_values.keys()
        if one_key.startswith(prefix)
    ]
    prefix_keys.sort(reverse=True)
    # print(prefix_keys)

    result = 0
    for one_key in prefix_keys:
        result = (result << 1) + wire_values[one_key]
    return result


gates_list: list[Gate] = []

for one_gate in gates.splitlines():
    gate_items = match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", one_gate)
    match gate_items[2]:
        case "AND":
            gates_list.append(AndGate(gate_items[1], gate_items[3], gate_items[4]))
        case "OR":
            gates_list.append(OrGate(gate_items[1], gate_items[3], gate_items[4]))
        case "XOR":
            gates_list.append(XorGate(gate_items[1], gate_items[3], gate_items[4]))


def resolve_gates(input_gates_list: list[Gate], values_dict: dict[str, int]) -> tuple[dict[str, int], dict[str, set]]:
    gates_list = deque(input_gates_list)
    values = values_dict.copy()
    deps = {}
    while len(gates_list) > 0:
        current_gate = gates_list.popleft()
        if not current_gate.check_gate(values, deps):
            # gate did not fire so put it back on the list
            gates_list.append(current_gate)
    return values, deps


x_val = wires_to_value("x", wire_values_dict)
print(f"{x_val}    {x_val:b}")
y_val = wires_to_value("y", wire_values_dict)
print(f"{y_val}    {y_val:b}")
print(f"{x_val+y_val}   {x_val+y_val:b}")

x_plus_y = x_val + y_val
x_plus_y_str = f"{x_plus_y:b}"

result_dict, result_deps = resolve_gates(gates_list, wire_values_dict)
# pprint(result_dict)
# pprint(result_deps)
z_val = wires_to_value("z", result_dict)
print(f"{z_val}   {z_val:06b}")
z_val_str = f"{z_val:b}"

diff = z_val - x_val - y_val
print(f"    {diff}   {diff:046b}")

for i in range(len(z_val_str)-1, -1, -1):
    if z_val_str[i] != x_plus_y_str[i]:
        last_diff = i

for i in range(0, len(z_val_str)):
    if z_val_str[i] != x_plus_y_str[i]:
        first_diff = i


# print(f"z{first_diff:02}")
# pprint(result_deps[f"z{first_diff:02}"])

# pprint(f"z{first_diff-1:02}")
# pprint(result_deps[f"z{first_diff-1:02}"])

pprint(result_deps[f"z{first_diff:02}"]-result_deps[f"z{last_diff:02}"])
