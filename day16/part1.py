import math
from util.grids import Direction, Grid, Point, cardinal_directions
from networkx import DiGraph
import networkx as nx

def solve(lines:list[str]):
    g = Grid(lines)
    start = g.get_matching_positions("S")[0]
    end = g.get_matching_positions("E")[0]
    maze_locations = g.get_matching_positions(".") + [start, end]

    # edges are not symetrical, therefore DiGraph
    maze_graph = DiGraph()
    for point in maze_locations:
        # a point is defined by it's x,y as well as the direction the reindeer is facing while standing on it
        # could be smarter and only add nodes that it would be possible to enter this node from
        # but unconnected nodes shouldnt affect performance too badly.
        maze_graph.add_node((point, Direction.NORTH))
        maze_graph.add_node((point, Direction.SOUTH))
        maze_graph.add_node((point, Direction.EAST))
        maze_graph.add_node((point, Direction.WEST))

    for point in maze_locations:
        # for each floor point, generate 4 surrounding points.
        # iterate over each orientation we could be facing on this square.
        # add edge to straightahead of cost 1 if that node is in graph
        # add edge to all other nodes of cost 1001 if that node is in the graph.
        
        for facing_dir in cardinal_directions:
            points_from_here = [(dir, Point(point.col + dir.value.col, point.row + dir.value.row)) for dir in cardinal_directions]
            for dir, point_from_here in points_from_here:
                if (point_from_here, dir) in maze_graph.nodes:
                    # 1 position ahead exists. add cost 1 edge
                    # cost = 1 if facing_dir == dir else 1001
                    maze_graph.add_edge((point, facing_dir), (point_from_here, dir), weight=(1 if facing_dir == dir else 1001))

    shortest_ending_len = math.inf
    for dir in cardinal_directions:
        # example can be finished either facing north or east.
        # my actual finish can only be reached facing east.
        # iterating over all options to make it generic
        try:
            shortest_path_to_end = nx.shortest_path_length(maze_graph, (start, Direction.EAST), (end, dir), weight="weight")
            print(f"dir: {dir}, len: {shortest_path_to_end}")
            if shortest_path_to_end < shortest_ending_len:
                shortest_ending_len = shortest_path_to_end
        except:
            pass

    print(f"shortest path: {shortest_ending_len}")