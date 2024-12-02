from day02.util import is_decreasing, is_increasing

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