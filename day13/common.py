from dataclasses import dataclass

@dataclass(frozen=True)
class Machine:
    a_button_x_increase: int
    a_button_y_increase: int
    b_button_x_increase: int
    b_button_y_increase: int
    prize_x: int
    prize_y: int

def solve_machine_simultaneous_equations(machine:Machine, a_cost:int, b_cost:int) -> int:
    # the equations were derived from:
    # Px = (a_button_x_increase * A) + (b_button_x_increase * B)
    # Py = (a_button_y_increase * A) + (b_button_y_increase * B)
    # rearranging the first equation to equal A, substituting the new A equation in to A in the second equation, 
    # then rearranging the second equation to solve for B.
    # This gives us one equation which equals B, which we have all the values to solve, and one equation solving for A, which we can solve
    # once we have the value of B.
    # This substitution method was performed on paper and the resulting equations are used here.
    b_numerator = (machine.prize_x * machine.a_button_y_increase) - (machine.a_button_x_increase * machine.prize_y)
    b_denominator = (machine.b_button_x_increase * machine.a_button_y_increase) - (machine.a_button_x_increase * machine.b_button_y_increase)
    b = b_numerator/b_denominator
    if b.is_integer(): # if b is not a whole number then we can bail before working out A
        a_numerator = machine.prize_y - (machine.b_button_y_increase * int(b))
        a_denominator = machine.a_button_y_increase

        a = a_numerator/a_denominator
        if a.is_integer():
            return (int(a) * a_cost) + (int(b) * b_cost)

    return 0