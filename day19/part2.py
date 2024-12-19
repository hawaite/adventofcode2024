from functools import cache

@cache
def get_available_towels(towel_str):
    # cant pass a list or a set as an argument to a memoized function due it being an unhashable type
    # so just making it fast to get the available towel list when inside the cached function
    # could also use global vars instead
    return set([x for x in towel_str.split(", ")])

@cache
def count_possible(required_design, towels_def_str):
    available_towels = get_available_towels(towels_def_str)
    
    # if the design is empty string, that means the entire thing was successfully consumed
    # which means this is a valid ordering and should count.
    if required_design == "":
        return 1 # an exact match results in a 1
    
    # from the list of allowed prefixes, get the ones which are valid for the required_design remaining
    valid_prefixes = [prefix_towel for prefix_towel in available_towels if required_design[:len(prefix_towel)] == prefix_towel]
    
    # if there were no valid prefixes, then immediately False because cannot continue
    if len(valid_prefixes) == 0:
        # print(f"no valid prefixes for {required_design}. Returning 0")
        return 0
    
    # for all the valid prefixes, recurse with the required design minus that prefix.
    # and sum all the times we found a valid ordering.
    return sum([ count_possible(required_design[len(prefix_towel):], towels_def_str) for prefix_towel in valid_prefixes])
        
def solve(lines:list[str]):
    total = 0

    for required_design in lines[2:]:
        total += count_possible(required_design, lines[0])

    print(f"total: {total}")