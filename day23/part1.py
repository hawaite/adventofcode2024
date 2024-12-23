import networkx as nx
from networkx import Graph

def solve(lines:list[str]):
    network = Graph()
    for line in lines:
        node_one, node_two = line.split("-")
        network.add_edge(node_one,node_two)

    cycles = nx.simple_cycles(network, length_bound=3)
    count = 0
    for cycle in cycles:
        if len([x for x in cycle if x[0] == "t"]) > 0:
            count += 1

    print(count)