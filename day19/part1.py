from functools import cache

@cache
def get_available_towels(towel_str):
    # cant pass a list or a set as an argument to a memoized function
    # so just making it fast to get the available towel list when inside the cached function
    # could also use global vars instead
    return set([x for x in towel_str.split(", ")])

@cache
def is_possible(required_design, towels_def_str):
    available_towels = get_available_towels(towels_def_str)
    # if remainder just exists in the available towel set, then immediately return True
    if required_design in available_towels:
        return True
    
    # from the list of allowed prefixes, get the ones which are valid for the required_design remaining
    valid_prefixes = [prefix_towel for prefix_towel in available_towels if required_design[:len(prefix_towel)] == prefix_towel]
    
    # if there were no valid prefixes, then immediately False because cannot continue
    if len(valid_prefixes) == 0:
        return False
    
    # for all the valid prefixes, recurse with the required design minus that prefix.
    results = [ is_possible(required_design[len(prefix_towel):], towels_def_str) for prefix_towel in valid_prefixes]
    # if any path returns True, then it is possible
    return any(results)
        
def solve(lines:list[str]):
    total = 0

    for required_design in lines[2:]:
        if is_possible(required_design, lines[0]):
            total += 1

    print(f"total: {total}")