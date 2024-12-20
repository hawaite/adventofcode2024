# gets all points ON the manhattan circle
from util.grids import Point, cardinal_directions


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

# takes the start and end points and returns both the next path tile for every node and
# a distance_to_the_finish value for every path node
def parse_path(start, end, path_tiles):
    current_node = end
    dist_so_far = 1
    visited = set()
    next_nodes = {end: None}
    dist = {end: 0}
    
    while current_node != start:
        visited.add(current_node)
        neighbours = [Point(current_node.col + dir.value.col, current_node.row + dir.value.row) for dir in cardinal_directions]
        # all neighbours which are path pieces which have not yet been visited.
        valid_neighbours = [p for p in neighbours if p in path_tiles and p not in visited]
        next_point = valid_neighbours[0]

        next_nodes[next_point] = current_node
        dist[next_point] = dist_so_far
        current_node = next_point
        dist_so_far += 1
    dist[start] = dist_so_far

    return (next_nodes, dist)

def get_number_of_cheated_paths_saving_100_ticks(start, end, distance_dict, next_node_dict, path_tiles, manhattan_radius):
    uncheated_distance = distance_dict[start]
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
        valid_points_to_check = [p for p in all_manhattan_distance_points(current_node, manhattan_radius) if p in path_tiles and p not in visited]

        for point in valid_points_to_check:
            # cheated distance is travelled distance so far 
            cheated_distance = dist_so_far + distance_dict[point] + manhattan_distance(current_node, point)
            if uncheated_distance - cheated_distance >= 100:
                paths_saving_100_or_more_ticks += 1

        # store the current node in visited so we dont try cheat backwards
        visited.add(current_node)
        dist_so_far += 1
        current_node = next_node_dict[current_node]
    return paths_saving_100_or_more_ticks