import os

def difference_is_between_inclusive(x, y, lower, upper):
    return abs(x - y) >= lower and abs(x - y) <= upper

def is_increasing(report: list[int]):
    for i in range(0,len(report) - 1):
        if not (report[i] < report[i+1] and difference_is_between_inclusive(report[i], report[i+1], 1, 3)):
            return False
    return True

def is_decreasing(report: list[int]):
    for i in range(0,len(report) - 1):
        if not (report[i] > report[i+1]and difference_is_between_inclusive(report[i], report[i+1], 1, 3)):
            return False
    return True

def solve(lines:list[str]):
    result = 0
    for line in lines:
        measurements = [int(x) for x in line.split(" ")]
        if is_increasing(measurements) or is_decreasing(measurements):
            result += 1

    print(result)

def main():
    cwd = os.path.dirname(__file__)

    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]

    solve(all_lines_stripped)

if __name__ == "__main__":
    main()