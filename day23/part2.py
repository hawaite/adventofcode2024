import networkx as nx
from networkx import Graph

def solve(lines:list[str]):
    network = Graph()
    for line in lines:
        node_one, node_two = line.split("-")
        network.add_edge(node_one,node_two)

    all_cliques = nx.clique.enumerate_all_cliques(network)
    largest_clique = []
    for clique in all_cliques:
        if len(clique) > len(largest_clique):
            largest_clique = clique

    print(largest_clique)
    print(",".join(sorted(largest_clique)))