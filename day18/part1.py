from networkx import shortest_path
import networkx as nx

def solve(lines:list[str]):
    width = 71
    height = 71 
    start = (0,0)
    target = (70,70)
    g = nx.grid_2d_graph(height, width)

    for line in lines[0:1024]:
        x, y = line.split(",")
        g.remove_node((int(x),int(y)))

    path = shortest_path(g, start, target)
    print(len(path) - 1) # minus 1 as first space doesnt count as a step
    