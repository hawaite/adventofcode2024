import math
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

def generate_directional_keypad_graph():
    directional_keypad = DiGraph()
    nx.add_path(directional_keypad, ["^", "A"], direction = ">")
    nx.add_path(directional_keypad, ["<", "V", ">"], direction = ">")

    nx.add_path(directional_keypad, reversed(["^", "A"]), direction = "<")
    nx.add_path(directional_keypad, reversed(["<", "V", ">"]), direction = "<")

    nx.add_path(directional_keypad, ["^", "V"], direction = "V")
    nx.add_path(directional_keypad, ["A", ">"], direction = "V")

    nx.add_path(directional_keypad, reversed(["^", "V"]), direction = "^")
    nx.add_path(directional_keypad, reversed(["A", ">"]), direction = "^")

    return directional_keypad

def path_to_direction_list(keypad, path):
    path_directions = []
    for source, dest in pairwise(path):
        path_directions.append(keypad[source][dest]["direction"])
    return path_directions

# flattens list of lists to a single level list
def flatten(l):
    return [item for sublist in l for item in sublist]

def get_all_paths(buttons, keypad):
    current = "A"
    parts = []
    for button in buttons:
        paths = list(nx.all_shortest_paths(keypad, current, button))
        direction_lists = [path_to_direction_list(keypad, x) for x in paths]
        direction_lists_plus_a = [dl + ["A"] for dl in direction_lists]
        parts.append(direction_lists_plus_a)
        current = button

    all_paths = []
    # EXTREMELY EXPENSIVE OPERATION
    # basically all of the execution time is flattening lists
    for p in list(product(*parts)):
        all_paths.append(flatten(p))
    return all_paths

def solve(lines:list[str]):
    directional_keypad = generate_directional_keypad_graph()
    numeric_keypad = generate_numeric_keypad_graph()
    total = 0

    for line in lines:
        minimum_level_3_len = math.inf
        minimum_level_3 = None

        lvl1_paths = get_all_paths(line, numeric_keypad)
        print(f"There were {len(lvl1_paths)} level 1 paths")

        lvl2_paths = []
        for lvl1_path in lvl1_paths:
            lvl2_paths.extend(get_all_paths(lvl1_path, directional_keypad))
        print(f"There were {len(lvl2_paths)} level 2 paths")

        lvl3_paths = []
        for lvl2_path in lvl2_paths:
            lvl3_paths.extend(get_all_paths(lvl2_path, directional_keypad))
        print(f"There were {len(lvl3_paths)} level 3 paths")

        for lvl3_path in lvl3_paths:
            if len(lvl3_path) < minimum_level_3_len:
                minimum_level_3_len = len(lvl3_path)
                minimum_level_3 = lvl3_path

        print(line)
        print(minimum_level_3_len)
        print(minimum_level_3)
        total += minimum_level_3_len * int(line[:-1])
        print("---------------")
    print(total)