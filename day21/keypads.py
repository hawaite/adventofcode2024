import networkx as nx
from networkx import DiGraph

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