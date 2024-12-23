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
        # a point is defined by it's x,y as well as the facing direction while you're 
        maze_graph.add_node((point, Direction.NORTH))
        maze_graph.add_node((point, Direction.SOUTH))
        maze_graph.add_node((point, Direction.EAST))
        maze_graph.add_node((point, Direction.WEST))

    for point in maze_locations:
        # for each point, generate 4 surrounding points.
        # iterate over each orientation we could be facing on this square.
        # add edge to any found valid locations with cost 1 if straight ahead, otherwise 1001
        
        for facing_dir in cardinal_directions:
            points_from_here = [(dir, Point(point.col + dir.value.col, point.row + dir.value.row)) for dir in cardinal_directions]
            for dir, point_from_here in points_from_here:
                if (point_from_here, dir) in maze_graph.nodes:
                    # target node exists in the graph. if its the same direction as current node then cost is 1, otherwise 1001
                    maze_graph.add_edge((point, facing_dir), (point_from_here, dir), weight=(1 if facing_dir == dir else 1001))

    shortest_ending_len = math.inf
    shortest_ending_direction = Direction.NORTH
    for dir in cardinal_directions:
        # example can be finished either facing north or east.
        # my actual finish can only be reached facing east.
        # iterating over all options to make it generic to all inputs
        try:
            shortest_path_to_end = nx.shortest_path_length(maze_graph, (start, Direction.EAST), (end, dir), weight="weight")
            if shortest_path_to_end < shortest_ending_len:
                shortest_ending_len = shortest_path_to_end
                shortest_ending_direction = dir
        except:
            pass

    print(f"shortest path: {shortest_ending_len}")
    print(f"shortest ending direction: {shortest_ending_direction}")

    # this gives every path with the same shortest length
    all_shortest_paths = nx.all_shortest_paths(maze_graph, (start, Direction.EAST), (end, shortest_ending_direction), weight="weight")
    
    # add all the used points to a set to get the total points in the grid used.
    used_node_set = set()

    for path in all_shortest_paths:
        for node in path:
            point,dir = node
            used_node_set.add(point)
    
    print(len(used_node_set))