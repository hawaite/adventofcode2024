import queue
from util.grids import Grid, Point, cardinal_directions

# gets all points ON the manhattan circle
def manhattan_distance_points(center, n):
    points = []
    for offset in range(0,n):
        invOffset = n - offset # Inverse offset
        points.append(Point(center.col + offset, center.row + invOffset))
        points.append(Point(center.col + invOffset, center.row - offset))
        points.append(Point(center.col - offset, center.row - invOffset))
        points.append(Point(center.col - invOffset, center.row + offset))
    return points

def all_manhattan_distance_points(center, n):
    points = set()
    for i in range(0,n):
        points = points.union(manhattan_distance_points(center, i+1))
    return points

def manhattan_distance(point_one, point_two):
    return abs(point_one.col - point_two.col) + abs(point_one.row - point_two.row)

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

    current_node = end
    dist_so_far = 1
    visited = set()
    next_nodes = {end: None}
    dist = {end: 0}
    
    while current_node != start:
        visited.add(current_node)
        neighbours = [Point(current_node.col + dir.value.col, current_node.row + dir.value.row) for dir in cardinal_directions]
        # all neighbours which are path pieces which have not yet been visited.
        valid_neighbours = [p for p in neighbours if p in paths and p not in visited]
        next_point = valid_neighbours[0]

        next_nodes[next_point] = current_node
        dist[next_point] = dist_so_far
        current_node = next_point
        dist_so_far += 1
    dist[start] = dist_so_far

    uncheated_distance = dist[start]
    current_node = start
    dist_so_far = 0
    visited = set()

    paths_saving_100_or_more_ticks = 0
    
    # now iterate the path forwards. For each point, get a manhattan circle around that point.
    # for each valid path tile in the manhattan circle that isnt behind us,
    # the cheated distance from that tile is the travelled distance along the official path
    # plus the distance from that point to the finish, plus the manhattan distance from the official
    # path point to the cheated point.
    while current_node != end:
        valid_points_to_check = [p for p in manhattan_distance_points(current_node, 2) if p in paths and p not in visited]

        for point in valid_points_to_check:
            # cheated distance is travelled distance so far 
            cheated_distance = dist_so_far + dist[point] + manhattan_distance(current_node, point)
            if uncheated_distance - cheated_distance >= 100:
                paths_saving_100_or_more_ticks += 1

        # store the current node in visited so we dont try cheat backwards
        visited.add(current_node)
        dist_so_far += 1
        current_node = next_nodes[current_node]

    print(f"paths_saving_100_or_more_ticks: {paths_saving_100_or_more_ticks}")
