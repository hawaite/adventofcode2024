from dataclasses import dataclass
from sympy.abc import a, b
import sympy as sp
from sympy.solvers import solve as sysolve

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
    lowest_cost = 10000000000000000
    eq1 = sp.Eq(machine.a_button_x_increase * a + machine.b_button_x_increase * b, machine.prize_x)
    eq2 = sp.Eq(machine.a_button_y_increase * a + machine.b_button_y_increase * b, machine.prize_y)
    results = sysolve([eq1, eq2], dict=True)
    for result in results:
        a_res = result.get(a)
        b_res = result.get(b)

        # cant have partial button presses
        if isinstance(a_res, sp.core.numbers.Integer) and isinstance(b_res, sp.core.numbers.Integer):
            cost = (int(a_res) * a_cost) + (int(b_res) * b_cost)
            if cost < lowest_cost:
                lowest_cost = cost
    
    if lowest_cost == 10000000000000000:
        return None
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
            int(prize_def[0][2:])+10000000000000 ,
            int(prize_def[1][2:])+10000000000000))
        line_ix += 4

    total_tokens = 0
    for machine in machines:
        print(machine)
        res = solve_machine(machine, a_button_cost, b_button_cost)
        print(res)
        if res is not None:
            total_tokens += res
    print(total_tokens)

