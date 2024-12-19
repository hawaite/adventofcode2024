import heapq
import itertools
from util.grids import Direction, Grid, Point, cardinal_directions

# if the move is in the direction we are pointing, cost is 1.
# otherwise the cost is 1001 (1 rotate + 1 move)
def cost(source, dest, direction):
    if dest == Point(source.col + direction.value.col, source.row + direction.value.row):
        return 1
    else:
        return 1001

def solve(lines:list[str]):
    g = Grid(lines)
    start = g.get_matching_positions("S")[0]
    end = g.get_matching_positions("E")[0]
    maze_locations = g.get_matching_positions(".") + [start, end]
    counter = itertools.count()

    # start at maze start location
    distances = {node: float('infinity') for node in maze_locations}
    prev = {node: None for node in maze_locations}
    distances[start] = 0
    
    pq = [(0, next(counter), start, Direction.EAST)]

    while len(pq) > 0:
        current_distance, _, current_point, current_direction = heapq.heappop(pq)

        if current_distance > distances[current_point]:
            continue

        if current_point == end:
            break

        all_neighbours = [(dir,Point(current_point.col + dir.value.col, current_point.row + dir.value.row)) for dir in cardinal_directions]
        # exclude wall points
        valid_neighbours = [p for p in all_neighbours if p[1] in maze_locations]

        for neighbour_dir, neighbour_point in valid_neighbours:
            proposed_distance = current_distance + cost(current_point, neighbour_point, current_direction)

            if proposed_distance < distances[neighbour_point]:
                prev[neighbour_point] = current_point
                distances[neighbour_point] = proposed_distance
                new_facing_direction = neighbour_dir

                heapq.heappush(pq, (proposed_distance, next(counter), neighbour_point, new_facing_direction))

    print(f"shortest distance to end: {distances[end]}")
    # # debug graph rendering
    # current = end
    # shortest_path = [end]
    # while True:
    #     current = prev[current]
    #     shortest_path.append(current)
    #     if current == start:
    #         break
    # print(g.render_positions(shortest_path,'#'))