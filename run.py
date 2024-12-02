from enum import Enum
import importlib
import os
import sys

class ExitStatus(Enum):
    EXIT_BAD_CLI_ARGS = 1

def main():
    if not ( len(sys.argv) in [3,4] ) or ( not sys.argv[1].isnumeric() ) or ( not sys.argv[2].isnumeric() ) or (int(sys.argv[2]) not in [1,2]):
        print("usage: python run.py <day_number> <1|2> [e]")
        print("  day_number (required) - day to run")
        print("  1|2 (required)        - run part 1 or 2")
        print("  e (optional)          - use example input rather than full input")
        exit(ExitStatus.EXIT_BAD_CLI_ARGS.value)

    use_example_file = False
    if len(sys.argv) == 4 and sys.argv[3] == "e":
        use_example_file = True

    part_number = int(sys.argv[2])
    day_number = int(sys.argv[1])
    day_zero_padded = "%02d" % day_number
    with_or_without_example_file = "with example input" if use_example_file else "with full input"
    print("Running day %s, part %d, %s" % (day_zero_padded, part_number, with_or_without_example_file))

    cwd = os.path.dirname(__file__)

    input_path = f"{cwd}/day{day_zero_padded}/input.txt" if not use_example_file else f"{cwd}/day{day_zero_padded}/example.txt"

    with(open(input_path, 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]

    solution = importlib.import_module("day%s.part%d"%(day_zero_padded, part_number))
    solution.solve(all_lines_stripped)

if __name__ == "__main__":
    main()