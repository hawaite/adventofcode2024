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