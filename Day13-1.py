from pprint import pprint
from re import search

from Inputs.Day13_input import problem_input


# problem_input = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
#
# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176
#
# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450
#
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279"""

# problem_input = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400"""

# A•AX + B•BX = X
# A•AY + B•BY = Y
#
# A•AX = X - B•BX
# A = (X - B•BX)/AX
# (X - B•BX)/AX • AY + B•BY = Y
# (X - B•BX)/AX + B•BY/AY = Y/AY
# X - B•BX + B•BY•AX/AY = Y•AX/AY
# B•BY•AX/AY - B•BX = Y•AX/AY - X
# B•(BY•AX/AY - BX) = Y•AX/AY - X
# B = (Y•AX/AY - X) / (BY•AX/AY - BX)
# B = (Y•AX - X•AY) / (BY•AX - BX•AY)
#
# B = (5400*94 - 8400*34)/(67*94 - 22*34)
#
# A = (8400 - 40*22)/94

def parse_input_section(input_section: str) -> dict[str, int]:
    result = {}
    lines = input_section.splitlines()
    match_a = search(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
    result["ax"] = int(match_a[1])
    result["ay"] = int(match_a[2])
    match_b = search(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
    result["bx"] = int(match_b[1])
    result["by"] = int(match_b[2])
    match_p = search(r"Prize: X=(\d+), Y=(\d+)", lines[2])
    result["x"] = int(match_p[1])
    result["y"] = int(match_p[2])

    return result


def calc_button_presses(game: dict[str, int]) -> dict[str, float]:
    b = (game["y"]*game["ax"] - game["x"]*game["ay"]) / (game["by"]*game["ax"] - game["bx"]*game["ay"])
    a = (game["x"] - b*game["bx"])/game["ax"]
    return {"a": a, "b": b}


def split_input_sections(prob_input: str) -> list[str]:
    result = prob_input.split("\n\n")
    return result


input_sections = split_input_sections(problem_input)
# pprint(input_sections)

cost = 0
for one_section in input_sections:
    game = parse_input_section(one_section)
    buttons = calc_button_presses(game)
    pprint(buttons)
    if buttons["a"] == int(buttons["a"]) and buttons["b"] == int(buttons["b"]):
        game_cost = buttons["a"]*3 + buttons["b"]
        print(f"least cost = {game_cost}")
        cost += game_cost
    else:
        print("Not possible")

print(f"cost = {cost}")

# game = parse_input_section(problem_input)
# pprint(game)
# buttons = calc_buttons(game)
# pprint(buttons)
