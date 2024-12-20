from day20.util import get_number_of_cheated_paths_saving_100_ticks, parse_path
from util.grids import Grid

def solve(lines:list[str]):
    track = Grid(lines)
    start = track.get_matching_positions("S")[0]
    end = track.get_matching_positions("E")[0]
    paths = track.get_matching_positions(".") + [start, end]

    # plan
    # start at the "end" point and work backwards until we get to start, building an adjacency dictionary and a
    # list of distances from that node to the end
    # Then we can traverse the path FORWARDS from the start node, counting distance from start, while at every node evaluating if theres a shortcut we can take
    # If there's a shortcut then the distance for that path is distance_so_far + distance_from_finish_of_target_node + manhattan distance to that node

    next_nodes, dist = parse_path(start,end,paths)
    paths_saving_100_or_more_ticks = get_number_of_cheated_paths_saving_100_ticks(start, end, dist, next_nodes, paths, 20)

    print(f"paths_saving_100_or_more_ticks: {paths_saving_100_or_more_ticks}")
