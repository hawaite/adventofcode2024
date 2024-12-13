from day13.common import Machine, solve_machine_simultaneous_equations

def solve(lines:list[str]):
    line_ix = 0
    machines:list[Machine] = []
    a_button_cost = 3
    b_button_cost = 1

    while line_ix < len(lines):
        button_a_def = lines[line_ix][10:].split(", ")
        button_b_def = lines[line_ix + 1][10:].split(", ")
        prize_def = lines[line_ix + 2][7:].split(", ")
        machines.append(Machine(
            int(button_a_def[0][2:]), 
            int(button_a_def[1][2:]),
            int(button_b_def[0][2:]),
            int(button_b_def[1][2:]),
            int(prize_def[0][2:]) + 10000000000000,
            int(prize_def[1][2:]) + 10000000000000))
        line_ix += 4

    total_tokens = sum([solve_machine_simultaneous_equations(m, a_button_cost, b_button_cost) for m in machines])
    print(total_tokens)

