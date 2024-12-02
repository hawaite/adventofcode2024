from day02.util import is_decreasing, is_increasing

def solve(lines:list[str]):
    result = 0
    for line in lines:
        measurements = [int(x) for x in line.split(" ")]
        if is_increasing(measurements) or is_decreasing(measurements):
            result += 1

    print(result)