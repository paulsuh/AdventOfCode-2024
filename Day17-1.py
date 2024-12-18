from pprint import pprint

from Inputs.Day17_input import register_a_init, register_b_init, register_c_init, program

register_a = register_a_init
register_b = register_b_init
register_c = register_c_init



# register_a = 0
# register_b = 0
# register_c = 0
# program = (0, 1, 2, 3)

instruction_pointer = 0
output = []


def combo(operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register_a
        case 5:
            return register_b
        case 6:
            return register_c
        case 7:
            raise RuntimeError("Got combo operand 7")


def adv(operand: int) -> None:
    global register_a

    denominator = 2 ** combo(operand)
    result = register_a // denominator
    register_a = result


def bxl(operand: int) -> None:
    global register_b

    register_b = register_b ^ operand


def bst(operand: int) -> None:
    global register_b

    register_b = combo(operand) % 8


def jnz(operand: int) -> None:
    global instruction_pointer

    if register_a != 0:
        instruction_pointer = operand - 2


def bxc(operand: int) -> None:
    global register_b
    global register_c

    register_b = register_b ^ register_c


def out(operand: int) -> None:
    output.append(combo(operand) % 8)


def bdv(operand: int) -> None:
    global register_a
    global register_b

    denominator = 2 ** combo(operand)
    result = register_a // denominator
    register_b = result


def cdv(operand: int) -> None:
    global register_a
    global register_c

    denominator = 2 ** combo(operand)
    result = register_a // denominator
    register_c = result


instructions = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def run_program(prog: tuple[int, ...]) -> None:
    global instruction_pointer

    while instruction_pointer < len(prog):
        op_code = prog[instruction_pointer]
        operand = prog[instruction_pointer + 1]
        instructions[op_code](operand)
        instruction_pointer += 2


# register_c = 9
# run_program((2, 6))
# print(register_b)

# register_a = 10
# run_program((5,0,5,1,5,4))
# print(output)

# register_a = 2024
# run_program((0,1,5,4,3,0))
# print(output)
# print(register_a)

# register_b = 29
# run_program((1,7))
# print(register_b)

# register_b = 2024
# register_c = 43690
# run_program((4,0))
# print(register_b)

# register_a = 729
# register_b = 0
# register_c = 0
#
# program = (0,1,5,4,3,0)
run_program(program)
print(",".join([
    str(i)
    for i in output
]))
