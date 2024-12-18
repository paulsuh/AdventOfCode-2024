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
    # if len(output) > len(program):
    #     raise RuntimeError("output exceeded program length")
    # if output != program[:len(output)]:
    #     raise RuntimeError("output cut short")


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


def run_program(prog: list[int]) -> None:
    global instruction_pointer

    while instruction_pointer < len(prog):
        op_code = prog[instruction_pointer]
        operand = prog[instruction_pointer + 1]
        instructions[op_code](operand)
        instruction_pointer += 2


def format_output(prog_out: list[int]) -> str:
    return ",".join([
        str(i)
        for i in prog_out
    ])


# register_a = 117440
# program = [0,3,5,4,3,0]

# result = run_program(program)
# print(result)


# for init_a in range(100000000):
#     register_a = init_a
#     register_b = 0
#     register_c = 0
#
#     instruction_pointer = 0
#     output = []
#
#     if init_a % 1000000 == 0:
#         print(init_a)
#
#     try:
#         run_program(program)
#
#         if output == program:
#             print(init_a)
#             print(format_output(output))
#             break
#
#     except RuntimeError:
#         pass
#         # print("!", end="")

# 2 4   register_a % 8 -> register_b                    a % 8 = b
# 1 5   register b ^ 5 -> register_b                    b ^ 5 = b 1 (001)
# 7 5   register_a // 2 ** register_b --> register_c    a // 2 ** b = c
# 1,6   register_b ^ 6 -> register_b                    b ^ 6 = b 4 (100)
# 0,3   register_a // 2 ** 3 --> register_a             a // 8 = a
# 4,1   register_b ^ register_c -> register_b           b ^ c = 2 (010)
# 5,5   output register_b
# 3,0   if register_a != 0, jump to 0

# b = (a % 8) ^ 5 ^ 6 ^ c
# c = a // 2 ** ((a % 8)^5)
# u = (a % 8) ^ 5

# 0 5
# 1 4
# 2 7
# 3 6
# 4 1
# 5 0
# 6 3
# 7 2


for a in range(8):
    print(a, a ^ 5)




program = [2,4,1,5,7,5,1,6,0,3,4,1,5,5]

for init_a in range(1000):
    register_a = init_a
    register_b = 0
    register_c = 0

    instruction_pointer = 0
    output = []

    run_program(program)
    if output[0] == 2:
        print(init_a, output)
