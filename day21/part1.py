import networkx as nx
from networkx import DiGraph
from itertools import pairwise, product

def generate_numeric_keypad_graph():
    number_keypad = DiGraph()
    nx.add_path(number_keypad, ["7", "8", "9"], direction = ">")
    nx.add_path(number_keypad, ["4", "5", "6"], direction = ">")
    nx.add_path(number_keypad, ["1", "2", "3"], direction = ">")
    nx.add_path(number_keypad, ["0", "A"], direction = ">")

    nx.add_path(number_keypad, reversed(["7", "8", "9"]), direction = "<")
    nx.add_path(number_keypad, reversed(["4", "5", "6"]), direction = "<")
    nx.add_path(number_keypad, reversed(["1", "2", "3"]), direction = "<")
    nx.add_path(number_keypad, reversed(["0", "A"]), direction = "<")

    nx.add_path(number_keypad, ["7", "4", "1"], direction = "V")
    nx.add_path(number_keypad, ["8", "5", "2", "0"], direction = "V")
    nx.add_path(number_keypad, ["9", "6", "3", "A"], direction = "V")

    nx.add_path(number_keypad, reversed(["7", "4", "1"]), direction = "^")
    nx.add_path(number_keypad, reversed(["8", "5", "2", "0"]), direction = "^")
    nx.add_path(number_keypad, reversed(["9", "6", "3", "A"]), direction = "^")

    return number_keypad

def path_to_direction_list(keypad, path):
    path_directions = []
    for source, dest in pairwise(path):
        path_directions.append(keypad[source][dest]["direction"])
    return path_directions

# flattens list of lists to a single level list
def flatten(l):
    return [item for sublist in l for item in sublist]

def get_all_numeric_paths(code):
    numeric_keypad = generate_numeric_keypad_graph()
    current = "A"
    parts = []
    for button in code:
        paths = list(nx.all_shortest_paths(numeric_keypad, current, button))
        direction_lists = [path_to_direction_list(numeric_keypad, x) for x in paths]
        direction_lists_plus_a = [dl + ["A"] for dl in direction_lists]
        parts.append(direction_lists_plus_a)
        current = button

    all_paths = []
    # EXTREMELY EXPENSIVE OPERATION
    # basically all of the execution time is flattening lists
    # print(parts)
    for p in list(product(*parts)):
        all_paths.append(flatten(p))
    return all_paths

# pre-computed shortest paths between directional buttons
# prefere options that have runs of the same direction, and heavily prefere options that do not end on a "<"
# as those cause the level above to be on "<" and have to travel back to "A"
shortest_directional = {
    ('^', 'A'): ['>'], 
    ('A', '^'): ['<'], 
    ('^', '<'): ['V', '<'], 
    ('<', '^'): ['>', '^'], 
    ('^', 'V'): ['V'], 
    ('V', '^'): ['^'], 
    ('^', '>'): ['>', 'V'],#[['>', 'V'], ['V', '>']], 
    ('>', '^'): ['<', '^'],#[['<', '^'], ['^', '<']], 
    ('A', '<'): ['V', '<', '<'],#[['<', 'V', '<'], ['V', '<', '<']], 
    ('<', 'A'): ['>', '>', '^'],#[['>', '>', '^'], ['>', '^', '>']], 
    ('A', 'V'): ['<', 'V'], #[['<', 'V'], ['V', '<']], 
    ('V', 'A'): ['>', '^'],#[['>', '^'], ['^', '>']], 
    ('A', '>'): ['V'], 
    ('>', 'A'): ['^'], 
    ('<', 'V'): ['>'], 
    ('V', '<'): ['<'], 
    ('<', '>'): ['>', '>'], 
    ('>', '<'): ['<', '<'], 
    ('V', '>'): ['>'], 
    ('>', 'V'): ['<'],
    ('^', '^'): [],
    ('<', '<'): [],
    ('>', '>'): [],
    ('V', 'V'): [],
    ('A', 'A'): [],
    }

def expand(code):
    current = "A"
    new_path = []
    for button in code:
        new_path.extend(shortest_directional[(current, button)])
        new_path.append("A")
        current = button
    return new_path

def solve(lines:list[str]):
    total = 0

    for line in lines:
        # somewhat expensive building of all possible paths between A, the three digits, and back to A
        lvl1_paths = get_all_numeric_paths(line)
        
        additional_levels = 2
        paths_to_evaluate = lvl1_paths

        for _ in range(0,additional_levels):
            paths = []
            for path in paths_to_evaluate:
                paths.append(expand(path))
            paths_to_evaluate = paths

        top_level_minimum_length = min([len(path) for path in paths_to_evaluate])
        total += top_level_minimum_length * int(line[:-1])
    print(total)