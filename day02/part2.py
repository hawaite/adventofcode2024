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

def is_valid_if_measurement_removed(measurements, level_to_remove):
    new_list = measurements.copy()
    del new_list[level_to_remove]
    return is_increasing(new_list) or is_decreasing(new_list)

def solve(lines:list[str]):
    result = 0
    for line in lines:
        measurements = [int(x) for x in line.split(" ")]
        if is_increasing(measurements) or is_decreasing(measurements):
            # already valid
            result += 1
        else:
            # check if can be made valid
            found_valid_result = False
            for i in range(0,len(measurements)):
                found_valid_result = found_valid_result or is_valid_if_measurement_removed(measurements,i)
            if found_valid_result:
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