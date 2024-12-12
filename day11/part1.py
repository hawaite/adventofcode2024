from day11.common import blink

def solve(lines:list[str]):
    step_count = 25
    digits = [int(x) for x in lines[0].split(" ")]

    # rock digits dont ever depend on each other.
    # that means we can just blink individual numbers to a certain degree and count the length.
    # then sum the calculated lengths
    print(sum([blink(x,step_count) for x in digits]))
