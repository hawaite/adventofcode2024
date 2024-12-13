from dataclasses import dataclass
from itertools import product
import sys
@dataclass(frozen=True)
class Machine:
    a_button_x_increase: int
    a_button_y_increase: int
    b_button_x_increase: int
    b_button_y_increase: int
    prize_x: int
    prize_y: int

# returns None is not solvable, otherwise returns minimized token counts
def solve_machine(machine:Machine, a_cost:int, b_cost:int) -> int|None:
    max_val = 2000000000000000
    all_options = product(range(0,101), range(0,101))
    lowest_cost = max_val
    for a_presses, b_presses in all_options:
        cost = (a_presses * a_cost) + (b_presses * b_cost)
        if lowest_cost != -1 and cost > lowest_cost:
            # we've already found a solution of some kind, 
            # #and this one would be more expensive
            continue

        x = (machine.a_button_x_increase * a_presses) + (machine.b_button_x_increase * b_presses)
        y = (machine.a_button_y_increase * a_presses) + (machine.b_button_y_increase * b_presses)
        if x == machine.prize_x and y == machine.prize_y and cost < lowest_cost:
            print(f"Found solution using {a_presses} A presses and {b_presses} B presses")
            lowest_cost = cost
    
    if lowest_cost == max_val:
        return None
    else:
        return lowest_cost
    

def solve(lines:list[str]):
    line_ix = 0
    machines:list[Machine] = []
    a_button_cost = 3
    b_button_cost = 1

    while line_ix < len(lines):
        button_a_def = lines[line_ix][10:].split(", ")
        button_b_def = lines[line_ix + 1][10:].split(", ")
        prize_def = lines[line_ix + 2][7:].split(", ")
        print(button_a_def)
        print(button_b_def)
        print(prize_def)
        machines.append(Machine(
            int(button_a_def[0][2:]), 
            int(button_a_def[1][2:]),
            int(button_b_def[0][2:]),
            int(button_b_def[1][2:]),
            int(prize_def[0][2:]),
            int(prize_def[1][2:])))
        line_ix += 4

    total_tokens = 0
    for machine in machines:
        print(machine)
        res = solve_machine(machine, a_button_cost, b_button_cost)
        if res is not None:
            total_tokens += res
    print(total_tokens)

