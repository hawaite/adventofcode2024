from networkx import shortest_path
import networkx as nx

def solve(lines:list[str]):
    width = 71
    height = 71 
    start = (0,0)
    target = (70,70)
    g = nx.grid_2d_graph(height, width)

    for line in lines:
        x, y = line.split(",")
        g.remove_node((int(x),int(y)))
        try:
            shortest_path(g, start, target)
        except nx.exception.NetworkXNoPath:
            print(f"No path available after removing point ({x},{y})")
            break    