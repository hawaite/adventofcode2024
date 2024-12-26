from functools import cache
import networkx as nx
from itertools import pairwise, permutations, product
from networkx import DiGraph

from day21.keypads import generate_directional_keypad_graph, generate_numeric_keypad_graph

def prune_zig_zags(direction_path_list):
    pruned_path_list = []

    for direction_path in direction_path_list:
        detected_change = False
        valid = True
        for node_one, node_two in pairwise(direction_path):
            if node_one != node_two:
                # detected a change for a second time
                if detected_change:
                    valid = False
                    break
                else:
                    detected_change = True
        if valid:
            pruned_path_list.append(direction_path)

    return pruned_path_list

def path_to_direction_string(keypad, path):
    path_directions = []
    for source, dest in pairwise(path):
        path_directions.append(keypad[source][dest]["direction"])
    return "".join(path_directions)

def get_shortest_paths_dict(keypad:DiGraph):
    paths = {}

    for source, dest in permutations(keypad.nodes,2):
        paths[(source,dest)] = prune_zig_zags([ path_to_direction_string(keypad, path) for path in nx.all_shortest_paths(keypad, source, dest) ])

    for node in keypad.nodes:
        paths[(node,node)] = [ "" ] # add a null path that does nothing
    return paths

# this will actually build a sequence for the key you give it
# important because some keypad moves have two options.
def build_sequence_options(buttons, shortest_keypad_paths):
    result_parts = []
    for previous_button, current_button in pairwise("A" + buttons):
        result_parts = result_parts + [shortest_keypad_paths[(previous_button,current_button)]] + [["A"]]
        previous_button = current_button

    return ["".join(x) for x in product(*result_parts)]


# this will chunk the input you give it in to segments delimited by "A" presses,
# and then will work out the shortest sequence of just that bit.
# Add together all the bits and you know the minimum sequence length for that whole input
@cache
def shortest_sequence_len(keys, depth):
    if depth == 0:
        # reached final depth, return the length of whatever the pattern at this level is
        return len(keys)
    
    # we can treat each segment ended by an "A" as its own isolated thing
    chunks = [part+"A" for part in keys.split("A")][:-1] # remove last "A" press that gets added

    # total is the sum of the minimum length of all the segments when evaluated to a depth.
    total = 0
    for chunk in chunks:
        dir_seq_options = build_sequence_options(chunk, shortest_directional_keypad_paths)
        total += min([ shortest_sequence_len(x, depth-1) for x in dir_seq_options ])

    return total

# globals
directional_keypad = generate_directional_keypad_graph()
numeric_keypad = generate_numeric_keypad_graph()
shortest_directional_keypad_paths = get_shortest_paths_dict(directional_keypad)
shortest_numeric_keypad_paths = get_shortest_paths_dict(numeric_keypad)

def solve(lines:list[str]):
    total = 0

    for line in lines:
        # build the sequence for the robot at level 0, on the numeric keypad
        numeric_sequence_options = build_sequence_options(line, shortest_numeric_keypad_paths)
        
        # for each option on the numeric sequence options (there may be multiple)
        # get the shortest path up 25 levels of keypads 
        shortest_seq_len = min([ shortest_sequence_len(x, 25) for x in numeric_sequence_options ])
        total += shortest_seq_len * int(line[:-1])
        
        # build_sequence_options_iter(line, shortest_numeric_keypad_paths)
    print(total)