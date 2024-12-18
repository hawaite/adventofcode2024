# this is just the entire day 17 input traslated in to a single line
# such that we dont incur any sort of emulation overhead.
# program is not self-modifying so we can get away with it
def execute_program(a):
    output = []
    while True:
        output.append( ((a % 8) ^ 3 ^ int(a / pow(2, ((a % 8) ^ 5)))) % 8 )
        a = int(a/8)
        if a == 0:
            break
    return output

# takes a value, multiplies it by 8, then adds a value between 0 and 7, then sees what the output of the "execute_program" function
# is if we set 'a' to that value. if the output values match the end of the program then thats an 'a' value we should continue to investigate.
def calculate_a(test_val, program):
    program_len = len(program)
    next_values_to_test = [ test_val * 8 + x for x in range(0,8)]
    next_results = [execute_program(a) for a in next_values_to_test]

    if program in next_results:
        ix = next_results.index(program)
        print(f"found value: {next_values_to_test[ix]}")
        exit()

    zipped = zip(next_values_to_test, next_results)

    matching_options = [x for x in zipped if x[1] == program[program_len - len(x[1]):]]

    for option in matching_options:
        calculate_a(option[0], program)

def solve(lines:list[str]):
    # only need the program for comparison as we have already translated it in to the function above
    program = [int(x) for x in lines[4].split(": ")[1].split(",")]

    # This was only solved through intuition and trial and error.
    # was working out a way to try reverse modulo, which involves multiplying by 8 and then adding a mystery value between 0 and 7.
    # continually multiplying by 8 and adding some value, while checking that we are generating the correct output digits
    # resulted in the correct answer.
    calculate_a(0, program)